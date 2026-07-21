"""
similarity.py
-------------
The core math of content-based filtering.

We use COSINE SIMILARITY as the primary metric:

    sim(a, b) = (a . b) / (||a|| * ||b||)

Why cosine and not Euclidean distance?
  * Our vectors mix several weighted blocks (audio / genre / text /
    popularity). Cosine cares about the *direction* (the "taste profile
    shape") of a vector, not its magnitude, so tracks with generally louder
    feature values aren't unfairly penalized against quieter ones.
  * Because every vector coming out of `FeatureStore` is already
    L2-normalized (see feature_engineering.py), cosine similarity reduces to
    a plain dot product: sim(a, b) = a . b. This is exactly what lets us use
    fast ANN libraries (HNSW) that are built around inner-product / L2
    search -- no runtime normalization needed.

Two similarity functions are provided:
  * `brute_force_topk`  - exact O(N*d) search. Fine for a few thousand items
    or for validating the ANN index's recall. Vectorized with a single
    matrix multiply.
  * `cosine_matrix`     - full pairwise similarity, only ever used on small
    slices (e.g. for offline evaluation / diversity metrics), never on the
    whole catalog (that would be O(N^2) and does not scale).
"""

from __future__ import annotations
import numpy as np


def brute_force_topk(query: np.ndarray, matrix: np.ndarray, k: int,
                      exclude: set[int] | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Exact top-k cosine search via a single matrix multiply.
    query: (d,) unit vector. matrix: (N, d) unit vectors (rows = items).
    Returns (indices, scores), both length k, sorted descending by score.
    """
    scores = matrix @ query  # cosine similarity since both are L2-normalized
    if exclude:
        scores = scores.copy()
        scores[list(exclude)] = -np.inf
    # argpartition for O(N) selection, then sort just the top-k
    k = min(k, len(scores))
    top_idx = np.argpartition(-scores, k - 1)[:k]
    top_idx = top_idx[np.argsort(-scores[top_idx])]
    return top_idx, scores[top_idx]


def cosine_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Pairwise cosine similarity between two small sets of unit vectors."""
    return a @ b.T


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))
