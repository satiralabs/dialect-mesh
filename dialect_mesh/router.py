"""
DialectMesh Router: Intent classification & slot extraction for East African languages.
Routes raw user speech/text to deterministic API tool calls.
"""

import re
from typing import Any, Dict, List, Optional, Tuple
from .normalizer import normalize_text
from .matcher import text_similarity


class IntentDefinition:
    def __init__(self, name: str, examples: List[str], tool_target: str, required_slots: Optional[List[str]] = None):
        self.name = name
        self.examples = examples
        self.tool_target = tool_target
        self.required_slots = required_slots or []


# Pre-configured domain intents for digital finance, health, and agriculture
DEFAULT_INTENTS = [
    IntentDefinition(
        name="transfer_money",
        examples=[
            # Amharic
            "ብር ላክ",
            "ገንዘብ ማስተላለፍ እፈልጋለሁ",
            "ለአቤል 500 ብር ላክለት",
            "ብር አስገባ",
            # Afaan Oromo
            "maallaqa ergi",
            "qarshii erguun barbaada",
            "herrega biraatti daddabarsi",
            # Kiswahili
            "tuma pesa",
            "nataka kutuma pesa kwa",
            "hamisha pesa",
        ],
        tool_target="banking.transfer_money",
        required_slots=["amount", "recipient"],
    ),
    IntentDefinition(
        name="check_balance",
        examples=[
            # Amharic
            "ሂሳቤን አሳየኝ",
            "ቀሪ ገንዘብ ስንት ነው",
            "ባላንስ እይ",
            # Afaan Oromo
            "hafna herrega koo naaf himi",
            "qarshii meeqatu hafe",
            # Kiswahili
            "angalia salio",
            "salio langu ni ngapi",
            "kiasi kilichobaki",
        ],
        tool_target="banking.check_balance",
    ),
    IntentDefinition(
        name="weather_crop_forecast",
        examples=[
            # Amharic
            "የአየር ሁኔታ ምን ይመስላል",
            "ዝናብ ይዘንባል ዛሬ",
            "የአዝመራ ዝናብ ትንበያ",
            # Afaan Oromo
            "haalli qilleensaa akkami",
            "bokkaan ni roobaa har'a",
            # Kiswahili
            "hali ya hewa leo ikoje",
            "mvua itanyesha leo",
        ],
        tool_target="agriculture.get_forecast",
    ),
    IntentDefinition(
        name="health_clinic_locator",
        examples=[
            # Amharic
            "የቅርብ ክሊኒክ የት አለ",
            "ሆስፒታል መሄድ እፈልጋለሁ",
            "ሀኪም ቤት የት ነው",
            # Afaan Oromo
            "hospitaalli dhihoo eessa jira",
            "manni yaalaa naannoo koo",
            # Kiswahili
            "hospitali ya karibu iko wapi",
            "zahanati iliyo karibu",
        ],
        tool_target="health.find_clinic",
    ),
]


class IntentRouter:
    """Routes normalized input to target intents and extracts entity slots."""

    def __init__(self, intents: Optional[List[IntentDefinition]] = None):
        self.intents = intents or DEFAULT_INTENTS

    def extract_slots(self, text: str) -> Dict[str, Any]:
        """Extract amounts, phone numbers, and potential entities."""
        slots: Dict[str, Any] = {}

        # 1. Number extraction (Arabic numerals)
        numbers = re.findall(r"\b\d+(?:\.\d+)?\b", text)
        if numbers:
            slots["amount"] = float(numbers[0]) if "." in numbers[0] else int(numbers[0])

        # 2. Ethiopian phone numbers (09..., 07..., +251...) or East African (+254...)
        phone_match = re.search(r"(\+?25[14]\d{8,9}|0[79]\d{8})", text)
        if phone_match:
            slots["recipient_phone"] = phone_match.group(1)

        return slots

    def route(self, raw_text: str, lang: str = "auto", threshold: float = 0.35) -> Dict[str, Any]:
        norm_query = normalize_text(raw_text, lang=lang)
        best_intent: Optional[IntentDefinition] = None
        best_score = 0.0
        best_example = ""

        for intent in self.intents:
            for example in intent.examples:
                norm_ex = normalize_text(example, lang=lang)
                score = text_similarity(norm_query, norm_ex)
                if score > best_score:
                    best_score = score
                    best_intent = intent
                    best_example = example

        slots = self.extract_slots(raw_text)

        if best_intent and best_score >= threshold:
            return {
                "matched": True,
                "intent": best_intent.name,
                "confidence": round(best_score, 4),
                "tool_target": best_intent.tool_target,
                "matched_example": best_example,
                "slots": slots,
                "normalized_query": norm_query,
            }

        return {
            "matched": False,
            "intent": "fallback_unknown",
            "confidence": round(best_score, 4),
            "tool_target": "system.ask_clarification",
            "slots": slots,
            "normalized_query": norm_query,
        }
