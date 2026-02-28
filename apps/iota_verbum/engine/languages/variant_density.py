from pprint import pprint

from .service import LanguageVariantService


def main() -> None:
    svc = LanguageVariantService()
    print("Languages:")
    for lang in svc.languages():
        print(f"- {lang.code}: {lang.name} ({lang.script})")

    print("\nVariants:")
    for v in svc.variants():
        print(f"- {v.id} @ {v.location} [{v.type}] witnesses={','.join(v.witnesses)}")

    print("\nVariant density by book:")
    pprint(svc.variant_density_by_book())


if __name__ == "__main__":
    main()
