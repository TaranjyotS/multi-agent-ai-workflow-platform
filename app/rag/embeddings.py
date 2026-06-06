import math
from collections import Counter


class LocalEmbeddingModel:
    """Deterministic lightweight embedding model for local development and tests."""
    def embed(self, text: str) -> list[float]:
        words = [w.lower().strip('.,:;!?()[]{}') for w in text.split() if w.strip()]
        counts = Counter(words)
        buckets = [0.0] * 64
        for word, count in counts.items():
            buckets[hash(word) % len(buckets)] += float(count)
        norm = math.sqrt(sum(x*x for x in buckets)) or 1.0
        return [x / norm for x in buckets]

def cosine(a: list[float], b: list[float]) -> float:
    if not a or not b:
        return 0.0
    return sum(x*y for x, y in zip(a, b, strict=False))
