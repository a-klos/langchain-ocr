"""Module to map language codes to language names using pycountry."""

import pycountry


def get_language_name_from_pycountry(code: str) -> str:
    """Given a language abbreviation (ISO 639-1), return the full language name in English using pycountry."""
    language = pycountry.languages.get(alpha_2=code.lower())
    if language:
        # Sometimes language.name may include extra parts, adjust as needed.
        return language.name.lower()
    return None


# Example usage:
if __name__ == "__main__":
    lang_codes = ["en", "de", "ru", "it", "es", "zh", "ja", "fr"]
    for lang_code in lang_codes:
        print(f"pycountry: {lang_code} -> {get_language_name_from_pycountry(lang_code)}")
