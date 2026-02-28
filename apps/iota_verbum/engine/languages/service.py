from collections import Counter
from typing import Dict, List

from .models import Language, Variant
from .repository import LanguageVariantRepository


class LanguageVariantService:
    def __init__(self, repo: LanguageVariantRepository | None = None) -> None:
        self.repo = repo or LanguageVariantRepository()

    def languages(self) -> List[Language]:
        return self.repo.load_languages()

    def variants(self) -> List[Variant]:
        return self.repo.load_variants()

    def variant_density_by_book(self) -> Dict[str, int]:
        """
        Very simple: assumes location starts with a book name (e.g. 'Mark 4:26').
        Returns counts of variants per book string.
        """
        counts: Counter[str] = Counter()
        for v in self.variants():
            book = v.location.split()[0]
            counts[book] += 1
        return dict(counts)
