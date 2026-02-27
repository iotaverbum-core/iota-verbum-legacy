from __future__ import annotations

import hashlib
import logging
import time

from app.llm.prompts import SYSTEM_PROMPT, build_user_prompt
from app.settings import get_settings

logger = logging.getLogger(__name__)


def _fallback_draft(modal: dict) -> str:
    distortion = modal.get("dominant_distortion", "fear")
    return (
        "[[G]] Christ is near in this moment.\n"
        "[[R]] Name what happened in one plain sentence.\n"
        f"[[D]] You are leaning toward {distortion}.\n"
        "[[H]] Take one slow breath and speak one honest line to Jesus.\n"
        "[[E]] Leave the outcome with the Lord."
    )


def generate_draft(
    entry_text: str,
    modal: dict,
    moment_mode: bool = False,
    use_llm: bool = True,
) -> str:
    settings = get_settings()
    if (not settings.openai_api_key) or (not use_llm):
        return _fallback_draft(modal)

    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key, timeout=settings.openai_timeout_seconds)
    user_prompt = build_user_prompt(entry_text=entry_text, modal=modal, moment_mode=moment_mode)
    max_tries = max(1, settings.openai_max_retries + 1)

    for attempt in range(max_tries):
        try:
            response = client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
            )
            text = response.choices[0].message.content.strip()
            if text:
                return text
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "llm generation failed",
                extra={
                    "attempt": attempt + 1,
                    "error": str(exc),
                    "entry_sha256": hashlib.sha256(entry_text.encode("utf-8")).hexdigest(),
                },
            )
            if attempt < max_tries - 1:
                time.sleep(0.35 * (attempt + 1))

    return _fallback_draft(modal)
