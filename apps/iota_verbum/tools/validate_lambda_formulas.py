#!/usr/bin/env python
"""
Validate Λ v0.1 formulas in a modal Bible file (`*.lambda.json`).

- Checks that every string in:
    - `identity_invariants[*]`
    - `units[*].statements[*].lambda_iv[*]`
  is a well-formed Λ v0.1 formula according to the core grammar:

    [] = □  (identity)
    <> = ◇  (enactment)
    EFF() = Δ (effect)
    !, &, |, -> as logical connectives
"""

from __future__ import annotations
import json
from pathlib import Path
import re
import sys
from typing import List


# -------------------------------
# Tokenizer
# -------------------------------

TOKEN_SPEC = [
    ("SPACE",   r"[ \t\n\r]+"),
    ("ARROW",   r"->|→"),
    ("AND",     r"&|∧"),
    ("OR",      r"\||∨"),
    ("NOT",     r"!|¬"),
    ("LBRACK",  r"\["),
    ("RBRACK",  r"\]"),
    ("LANGLE",  r"<"),
    ("RANGLE",  r">"),
    ("LPAREN",  r"\("),
    ("RPAREN",  r"\)"),
    ("COMMA",   r","),
    ("STRING",  r'"[^"]*"'),
    ("NUMBER",  r"\d+"),
    ("IDENT",   r"[A-Za-z_][A-Za-z0-9_]*"),
    ("UNICODE", r"[□◇Δ]"),
    ("OTHER",   r"."),
]

MASTER_PAT = re.compile("|".join("(?P<%s>%s)" % pair for pair in TOKEN_SPEC))

MODAL_FUNCS = {"EFF"}  # EFF(...) is treated as Δ(...) modal operator


class Token:
    __slots__ = ("type", "value")

    def __init__(self, t: str, v: str) -> None:
        self.type = t
        self.value = v

    def __repr__(self) -> str:
        return f"Token({self.type}, {self.value!r})"


def tokenize(s: str) -> List["Token"]:
    tokens: List[Token] = []
    for mo in MASTER_PAT.finditer(s):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "SPACE":
            continue
        if kind == "UNICODE":
            # Map pretty symbols to ASCII tokens
            if value == "□":
                tokens.append(Token("LBRACK", "["))
                tokens.append(Token("RBRACK", "]"))
                continue
            if value == "◇":
                tokens.append(Token("LANGLE", "<"))
                tokens.append(Token("RANGLE", ">"))
                continue
            if value == "Δ":
                tokens.append(Token("IDENT", "EFF"))
                continue
        tokens.append(Token(kind, value))
    return tokens


# -------------------------------
# Recursive descent parser
# -------------------------------

class ParserError(Exception):
    pass


class Parser:
    def __init__(self, tokens: List[Token]) -> None:
        self.tokens = tokens
        self.pos = 0

    def _peek(self, *types: str) -> bool:
        if self.pos >= len(self.tokens):
            return False
        tok = self.tokens[self.pos]
        return tok.type in types or tok.value in types

    def _expect(self, *types: str) -> Token:
        if self.pos >= len(self.tokens):
            raise ParserError(f"Unexpected end of input, expected {types}")
        tok = self.tokens[self.pos]
        if tok.type in types or tok.value in types:
            self.pos += 1
            return tok
        raise ParserError(f"Unexpected token {tok}, expected {types}")

    def parse_formula(self):
        node = self._parse_implication()
        if self.pos != len(self.tokens):
            raise ParserError(f"Extra tokens at end: {self.tokens[self.pos:]}")
        return node

    # <Implication> ::= <OrExpr> [ "->" <Implication> ]
    def _parse_implication(self):
        left = self._parse_or()
        if self._peek("ARROW"):
            self._expect("ARROW")
            right = self._parse_implication()
            return ("imp", left, right)
        return left

    # <OrExpr> ::= <AndExpr> { ("|" | "∨") <AndExpr> }
    def _parse_or(self):
        node = self._parse_and()
        while self._peek("OR"):
            self._expect("OR")
            right = self._parse_and()
            node = ("or", node, right)
        return node

    # <AndExpr> ::= <UnaryExpr> { ("&" | "∧") <UnaryExpr> }
    def _parse_and(self):
        node = self._parse_unary()
        while self._peek("AND"):
            self._expect("AND")
            right = self._parse_unary()
            node = ("and", node, right)
        return node

    # <UnaryExpr> ::= [ "!" | "¬" ] <UnaryExpr> | <ModalExpr> | <Primary>
    def _parse_unary(self):
        if self._peek("NOT"):
            self._expect("NOT")
            expr = self._parse_unary()
            return ("not", expr)

        # []φ
        if self._peek("LBRACK"):
            self._expect("LBRACK")
            self._expect("RBRACK")
            primary = self._parse_primary()
            return ("box", primary)

        # <>φ
        if self._peek("LANGLE"):
            self._expect("LANGLE")
            self._expect("RANGLE")
            primary = self._parse_primary()
            return ("diamond", primary)

        # EFF(φ)
        if self._peek("IDENT") and self.tokens[self.pos].value in MODAL_FUNCS:
            self._expect("IDENT")
            self._expect("LPAREN")
            inner = self._parse_implication()
            self._expect("RPAREN")
            return ("eff", inner)

        return self._parse_primary()

    # <Primary> ::= <Atomic> | "(" <Formula> ")"
    def _parse_primary(self):
        if self._peek("LPAREN"):
            self._expect("LPAREN")
            expr = self._parse_implication()
            self._expect("RPAREN")
            return expr
        return self._parse_atomic()

    # <Atomic> ::= <Predicate> "(" [ <TermList> ] ")"
    def _parse_atomic(self):
        tok = self._expect("IDENT")
        pred = tok.value
        if self._peek("LPAREN"):
            self._expect("LPAREN")
            terms = []
            if not self._peek("RPAREN"):
                terms.append(self._parse_term())
                while self._peek("COMMA"):
                    self._expect("COMMA")
                    terms.append(self._parse_term())
            self._expect("RPAREN")
            return ("pred", pred, terms)
        else:
            return ("pred", pred, [])

    # <Term> ::= <IDENT> ["(" <TermList> ")"] | <STRING> | <NUMBER>
    def _parse_term(self):
        if self._peek("IDENT"):
            tok = self._expect("IDENT")
            ident = tok.value
            if self._peek("LPAREN"):
                self._expect("LPAREN")
                args = []
                if not self._peek("RPAREN"):
                    args.append(self._parse_term())
                    while self._peek("COMMA"):
                        self._expect("COMMA")
                        args.append(self._parse_term())
                self._expect("RPAREN")
                return ("fun", ident, args)
            return ("ident", ident)

        if self._peek("STRING"):
            tok = self._expect("STRING")
            return ("string", tok.value)

        if self._peek("NUMBER"):
            tok = self._expect("NUMBER")
            return ("number", tok.value)

        raise ParserError(f"Unexpected token in term: {self.tokens[self.pos]}")


def parse_formula(formula: str):
    tokens = tokenize(formula)
    parser = Parser(tokens)
    return parser.parse_formula()


# -------------------------------
# JSON walker
# -------------------------------

def iter_lambda_strings(modal_json: dict):
    # identity_invariants
    for idx, s in enumerate(modal_json.get("identity_invariants", [])):
        if isinstance(s, str):
            yield ("identity_invariants", idx, s)

    # units[*].statements[*].lambda_iv[*]
    for unit in modal_json.get("units", []):
        uid = unit.get("id", "<no_unit_id>")
        for st in unit.get("statements", []):
            sid = st.get("id", "<no_statement_id>")
            for idx, s in enumerate(st.get("lambda_iv", [])):
                if isinstance(s, str):
                    yield (f"{uid}.{sid}.lambda_iv", idx, s)


def validate_modal_file(path: Path) -> bool:
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    ok = True
    for location, idx, formula in iter_lambda_strings(data):
        if not formula.strip():
            continue
        try:
            parse_formula(formula)
        except ParserError as e:
            ok = False
            print(f"[ERROR] {path} :: {location}[{idx}]")
            print(f"        Λ formula: {formula}")
            print(f"        Reason: {e}")
            print()
    if ok:
        print(f"[OK] All Λ formulas valid in {path}")
    return ok


# -------------------------------
# CLI
# -------------------------------

def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: python tools/validate_lambda_formulas.py <path-to-lambda-json> [more-files...]")
        return 1

    exit_code = 0
    for arg in argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"[WARN] File not found: {path}")
            exit_code = 1
            continue
        if not validate_modal_file(path):
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
