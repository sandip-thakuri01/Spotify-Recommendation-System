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

`matrix` may be a dense numpy array OR a scipy.sparse matrix (e.g. if the
feature store includes a sparse genre/text block). Both are supported here;
the sparse-vs-dense handling is centralized in this file so callers never
have to think about it.

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


def _to_dense_vector(x) -> np.ndarray:
    """Coerce a single feature row (dense ndarray OR sparse matrix row)
    into a flat, dense 1-D numpy array.

    Sparse matrices keep row-slices 2-D (shape (1, d)) instead of
    collapsing to 1-D the way numpy does, and some scipy ops return
    np.matrix instead of ndarray -- both cases are normalized here so
    downstream matmuls never silently produce the wrong shape.
    """
    if hasattr(x, "toarray"):
        x = x.toarray()
    x = np.asarray(x)
    return x.reshape(-1)


def brute_force_topk(query: np.ndarray, matrix, k: int,
                      exclude: set[int] | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Exact top-k cosine search via a single matrix multiply.
    query: (d,) unit vector (dense or sparse row -- will be densified).
    matrix: (N, d) unit vectors (rows = items); dense ndarray or scipy sparse.
    Returns (indices, scores), both length k, sorted descending by score.
    """
    query = _to_dense_vector(query)

    scores = matrix @ query  # cosine similarity since both are L2-normalized
    scores = np.asarray(scores).reshape(-1)  # normalize sparse/np.matrix output to 1-D ndarray

    if exclude:
        scores = scores.copy()
        valid = [i for i in exclude if 0 <= i < len(scores)]
        scores[valid] = -np.inf

    # argpartition for O(N) selection, then sort just the top-k
    k = min(k, len(scores))
    top_idx = np.argpartition(-scores, k - 1)[:k]
    top_idx = top_idx[np.argsort(-scores[top_idx])]
    return top_idx, scores[top_idx]


def cosine_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Pairwise cosine similarity between two small sets of unit vectors."""
    a = a.toarray() if hasattr(a, "toarray") else np.asarray(a)
    b = b.toarray() if hasattr(b, "toarray") else np.asarray(b)
    return a @ b.T


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(_to_dense_vector(a), _to_dense_vector(b)))
