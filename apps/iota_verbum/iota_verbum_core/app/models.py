from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Book(Base):
    __tablename__ = "books"
    book_code = Column(String, primary_key=True)
    canon_pos = Column(Integer)
    name_en = Column(String)
    language = Column(String)
    testament = Column(String)


class Unit(Base):
    __tablename__ = "units"
    unit_id = Column(String, primary_key=True)
    book_code = Column(String, ForeignKey("books.book_code"))
    chapter = Column(Integer)
    verse = Column(Integer)
    sub_id = Column(String, nullable=True)
    unit_type = Column(String)
    base_ref = Column(String, nullable=True)
    canonical_label = Column(String, nullable=True)
    book = relationship("Book", backref="units")


class Token(Base):
    __tablename__ = "tokens"
    token_id = Column(String, primary_key=True)
    unit_id = Column(String, ForeignKey("units.unit_id"))
    position = Column(Integer)
    surface = Column(String)
    normalized = Column(String)
    lemma_id = Column(String)
    lemma_gloss_en = Column(String, nullable=True)
    morph_code = Column(String)
    pos = Column(String, nullable=True)
    strongs = Column(String, nullable=True)
    unit = relationship("Unit", backref="tokens")


class Pericope(Base):
    __tablename__ = "pericopes"
    pericope_id = Column(String, primary_key=True)
    book_code = Column(String, ForeignKey("books.book_code"))
    start_unit_id = Column(String)
    end_unit_id = Column(String)
    title_en = Column(String)
    title_iota = Column(String)
    genre = Column(String)
    book = relationship("Book", backref="pericopes")


class Witness(Base):
    __tablename__ = "witnesses"
    witness_id = Column(String, primary_key=True)
    siglum = Column(String, unique=True, index=True)
    description = Column(String)
    family = Column(String, nullable=True)


class VariantSite(Base):
    __tablename__ = "variant_sites"
    site_id = Column(String, primary_key=True)
    unit_id = Column(String, ForeignKey("units.unit_id"))
    position_hint = Column(String, nullable=True)
    note = Column(String, nullable=True)
    unit = relationship("Unit", backref="variant_sites")


class Variant(Base):
    __tablename__ = "variants"
    variant_id = Column(String, primary_key=True)
    site_id = Column(String, ForeignKey("variant_sites.site_id"))
    reading_key = Column(String)
    reading_text = Column(Text)
    relation = Column(String, nullable=True)
    site = relationship("VariantSite", backref="variants")


class VariantSupport(Base):
    __tablename__ = "variant_support"
    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(String, ForeignKey("variants.variant_id"))
    witness_id = Column(String, ForeignKey("witnesses.witness_id"))
    support_level = Column(String)
    weight = Column(Float)
    variant = relationship("Variant", backref="support")
    witness = relationship("Witness")


class IVPair(Base):
    __tablename__ = "iv_pairs"
    iv_id = Column(String, primary_key=True)
    book_code = Column(String, ForeignKey("books.book_code"))
    scope = Column(String)
    pericope_id = Column(String, ForeignKey("pericopes.pericope_id"), nullable=True)
    primary_arc_id = Column(String, nullable=True)
    box_label = Column(String)
    box_description = Column(Text)
    diamond_label = Column(String)
    diamond_description = Column(Text)
    delta_label = Column(String)
    delta_description = Column(Text)
    textual_confidence = Column(Float, nullable=True)
    interpretive_confidence = Column(Float, nullable=True)
    summary = Column(Text, nullable=True)


class IVPairUnit(Base):
    __tablename__ = "iv_pair_units"
    id = Column(Integer, primary_key=True, autoincrement=True)
    iv_id = Column(String, ForeignKey("iv_pairs.iv_id"))
    unit_id = Column(String, ForeignKey("units.unit_id"))


class CanonicalArc(Base):
    __tablename__ = "canonical_arcs"
    arc_id = Column(String, primary_key=True)
    label = Column(String)
    description = Column(Text)
    links = Column(Text)  # simple JSON string of references
