"""
DialectMesh Normalizer: Orthographic, phonetic, and unicode normalization
for East African and low-resource languages.
"""

import re
import unicodedata
from typing import Dict

# Amharic / Ge'ez homophone mappings (conflating distinct historical glyphs into canonical forms)
AMHARIC_HOMOPHONE_MAP: Dict[str, str] = {
    # Ha variants: ሐ (0x1210-0x1217), ኀ (0x1280-0x1287) -> ሀ (0x1200-0x1207)
    "ሐ": "ሀ", "ሑ": "ሁ", "ሒ": "ሂ", "ሓ": "ሃ", "ሔ": "ሄ", "ሕ": "ህ", "ሖ": "ሆ",
    "ኀ": "ሀ", "ኁ": "ሁ", "ኂ": "ሂ", "ኃ": "ሃ", "ኄ": "ሄ", "ኅ": "ህ", "ኆ": "ሆ",
    # Se variants: ሠ (0x1220-0x1227) -> ሰ (0x1230-0x1237)
    "ሠ": "ሰ", "ሡ": "ሱ", "ሢ": "ሲ", "ሣ": "ሳ", "ሤ": "ሴ", "ሥ": "ስ", "ሦ": "ሶ",
    # Tze variants: ፀ (0x1340-0x1347) -> ጸ (0x1338-0x133F)
    "ፀ": "ጸ", "ፁ": "ጹ", "ፂ": "ጺ", "ፃ": "ጻ", "ፄ": "ጼ", "ፅ": "ጽ", "ፆ": "ጾ",
    # A variants: ዓ (0x12D0-0x12D7) -> አ (0x12a0-0x12a7)
    "ዓ": "አ", "ዑ": "ኡ", "ዒ": "ኢ", "ዓ": "ኣ", "ዔ": "ኤ", "ዕ": "እ", "ዖ": "ኦ",
}

# Ge'ez punctuation mapping to ASCII equivalents
GEEZ_PUNCTUATION_MAP: Dict[str, str] = {
    "፡": " ",  # word separator
    "።": ".",  # full stop
    "፣": ",",  # comma
    "፤": ";",  # semicolon
    "፥": ":",  # colon
    "፦": ":",  # preface colon
    "፧": "?",  # question mark
    "፨": "\n", # paragraph separator
}


def normalize_amharic(text: str) -> str:
    """Normalize Amharic text by harmonizing homophones, spaces, and punctuation."""
    if not text:
        return ""
    # NFC normalization
    text = unicodedata.normalize("NFC", text)
    # Map Ge'ez punctuation
    for p, replacement in GEEZ_PUNCTUATION_MAP.items():
        text = text.replace(p, replacement)
    # Map homophones
    for src, dst in AMHARIC_HOMOPHONE_MAP.items():
        text = text.replace(src, dst)
    # Collapse multiple whitespaces
    text = re.sub(r"\s+", " ", text).strip().lower()
    return text


def normalize_oromo(text: str) -> str:
    """Normalize Afaan Oromo text (Qubee Latin script): normalize glottal stops / hudhaa and case."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text).lower()
    # Normalize various apostrophe glyphs to standard straight apostrophe
    text = re.sub(r"[\u2018\u2019\u0060\u00B4]", "'", text)
    # Collapse repeating punctuation
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_swahili(text: str) -> str:
    """Normalize Kiswahili text: case, whitespaces, and standard Latin contractions."""
    if not text:
        return ""
    text = unicodedata.normalize("NFC", text).lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_text(text: str, lang: str = "auto") -> str:
    """General dispatcher based on detected or specified language."""
    if not text:
        return ""
    if lang == "am" or (lang == "auto" and any("\u1200" <= c <= "\u137F" for c in text)):
        return normalize_amharic(text)
    elif lang == "om":
        return normalize_oromo(text)
    elif lang == "sw":
        return normalize_swahili(text)
    else:
        return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip().lower()
