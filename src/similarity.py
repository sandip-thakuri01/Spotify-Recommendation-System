

from __future__ import annotations
import numpy as np


def _to_dense_vector(x) -> np.ndarray:
   
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
