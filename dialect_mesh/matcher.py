"""
DialectMesh Matcher: Sub-word character n-gram similarity & phonetic matcher.
Computes fast cosine/Jaccard similarity on edge CPU without GPU or torch.
"""

from collections import Counter
import math
from typing import Dict, List, Set, Tuple


def char_ngrams(text: str, n: int = 3) -> List[str]:
    """Generate padded character n-grams for robust low-resource matching."""
    padded = f"^{text}$"
    if len(padded) < n:
        return [padded]
    return [padded[i : i + n] for i in range(len(padded) - n + 1)]


def cosine_similarity(counter1: Counter, counter2: Counter) -> float:
    """Cosine similarity between two frequency vectors."""
    intersection = set(counter1.keys()) & set(counter2.keys())
    numerator = sum(counter1[x] * counter2[x] for x in intersection)

    sum1 = sum(v ** 2 for v in counter1.values())
    sum2 = sum(v ** 2 for v in counter2.values())
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    return numerator / denominator


def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Jaccard index between two token sets."""
    if not set1 or not set2:
        return 0.0
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0.0


def text_similarity(text1: str, text2: str, n: int = 3) -> float:
    """
    Combined weighted metric (0.7 * Cosine + 0.3 * Jaccard) on character n-grams.
    Proven effective for morphological variations in agglutinative/inflected languages.
    """
    grams1 = char_ngrams(text1, n)
    grams2 = char_ngrams(text2, n)

    c1 = Counter(grams1)
    c2 = Counter(grams2)
    s1 = set(grams1)
    s2 = set(grams2)

    cos_sim = cosine_similarity(c1, c2)
    jac_sim = jaccard_similarity(s1, s2)

    return (0.7 * cos_sim) + (0.3 * jac_sim)
