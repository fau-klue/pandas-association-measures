"""comparison of ranked lists

rbo implementation based on https://github.com/changyaochen/rbo/blob/master/rbo/rbo.py

"""

from tqdm import tqdm


def rbo(S, T, k=None, p=.95, ext=True, verbose=False):
    """
    Compute Rank-Biased Overlap (RBO) between two ranked lists S and T.

    Args:
        S (list or np.ndarray): First ranked list.
        T (list or np.ndarray): Second ranked list.
        k (int, optional): Depth of evaluation. Defaults to min(len(S), len(T)).
        p (float, optional): Weight parameter (0 < p < 1). Defaults to 1.0.
        ext (bool, optional): Whether to extrapolate RBO. Defaults to True.
        verbose (bool, optional): Print intermediate results. Defaults to False.

    Returns:
        float: Rank-Biased Overlap (RBO) score.
    """
    if not S and not T:
        return 1.0  # Both lists are empty

    if not S or not T:
        return 0.0  # One list is empty

    if k is None:
        k = min(len(S), len(T))
    k = min(len(S), len(T), k)

    if p <= 0 or p > 1:
        raise ValueError("p must be between 0 (exclusive) and 1")

    # Initialize agreement and average overlap arrays
    A, AO = [0] * k, [0] * k
    weights = [1.0 * (1 - p) * p**d for d in range(k)] if p != 1.0 else [1.0] * k

    S_running, T_running = {S[0]}, {T[0]}
    A[0] = 1 if S[0] == T[0] else 0
    AO[0] = weights[0] * A[0] if p != 1.0 else A[0]

    for d in tqdm(range(1, k), disable=not verbose):
        overlap = int(S[d] in T_running) + int(T[d] in S_running) + int(S[d] == T[d])
        A[d] = ((A[d - 1] * d) + overlap) / (d + 1)
        AO[d] = AO[d - 1] + weights[d] * A[d] if p != 1.0 else ((AO[d - 1] * d) + A[d]) / (d + 1)
        S_running.add(S[d])
        T_running.add(T[d])

    rbo_score = AO[-1] + A[-1] * p**k if ext and p < 1 else AO[-1]
    return max(0.0, min(1.0, rbo_score))
