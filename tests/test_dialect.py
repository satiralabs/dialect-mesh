"""
Tests for DialectMesh: Homophone normalization, similarity scoring, and intent routing.
"""

import unittest
from dialect_mesh.normalizer import normalize_amharic, normalize_oromo, normalize_swahili
from dialect_mesh.matcher import text_similarity
from dialect_mesh.router import IntentRouter


class TestDialectMesh(unittest.TestCase):
    def test_amharic_homophone_normalization(self):
        # ሐመር ሀ (ሐ) and ሆሄ ሀ should normalize to identical forms
        norm1 = normalize_amharic("ሐኪም ቤት")
        norm2 = normalize_amharic("ሀኪም ቤት")
        self.assertEqual(norm1, norm2)

        # ሰ vs ሠ
        self.assertEqual(normalize_amharic("ሠላም"), normalize_amharic("ሰላም"))

    def test_oromo_apostrophe_normalization(self):
        norm1 = normalize_oromo("har’a")
        norm2 = normalize_oromo("har'a")
        self.assertEqual(norm1, norm2)

    def test_routing_amharic_transfer(self):
        router = IntentRouter()
        res = router.route("ለአቤል 300 ብር ላክለት")
        self.assertTrue(res["matched"])
        self.assertEqual(res["intent"], "transfer_money")
        self.assertEqual(res["tool_target"], "banking.transfer_money")
        self.assertEqual(res["slots"].get("amount"), 300)

    def test_routing_oromo_balance(self):
        router = IntentRouter()
        res = router.route("qarshii meeqatu hafe herrega koo")
        self.assertTrue(res["matched"])
        self.assertEqual(res["intent"], "check_balance")

    def test_routing_swahili_weather(self):
        router = IntentRouter()
        res = router.route("hali ya hewa leo")
        self.assertTrue(res["matched"])
        self.assertEqual(res["intent"], "weather_crop_forecast")


if __name__ == "__main__":
    unittest.main()
