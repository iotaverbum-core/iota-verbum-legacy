from collections import Counter, defaultdict
from typing import Any, Dict, List

from fastapi import APIRouter

from engine.languages.models import Language
from engine.languages.service import LanguageVariantService

router = APIRouter(prefix="/languages", tags=["languages"])
service = LanguageVariantService()


@router.get("/", response_model=List[Language])
def list_languages() -> List[Language]:
    """
    Real languages list (backed by LanguageVariantService).
    """
    return service.languages()


@router.get("/variants")
def list_variants() -> List[Dict[str, Any]]:
    """
    Real variant summary grouped by language.
    """
    variants = service.variants()
    language_names = {lang.code: lang.name for lang in service.languages()}

    counts: Counter[str] = Counter()
    ids_by_language: Dict[str, List[str]] = defaultdict(list)
    for variant in variants:
        counts[variant.language] += 1
        ids_by_language[variant.language].append(variant.id)

    return [
        {
            "language": language_code,
            "name": language_names.get(language_code, language_code),
            "variant_count": count,
            "variant_ids": sorted(ids_by_language.get(language_code, [])),
        }
        for language_code, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]


@router.get("/variants/density")
def variant_density() -> Dict[str, int]:
    """
    Variant density by book.
    """
    return service.variant_density_by_book()
