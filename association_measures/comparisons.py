"""comparison of ranked lists

RBO implementation based on https://github.com/changyaochen/rbo/blob/master/rbo/rbo.py

"""

import numpy as np


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

    for d in range(1, k):
        overlap = int(S[d] in T_running) + int(T[d] in S_running) + int(S[d] == T[d])
        A[d] = ((A[d - 1] * d) + overlap) / (d + 1)
        AO[d] = AO[d - 1] + weights[d] * A[d] if p != 1.0 else ((AO[d - 1] * d) + A[d]) / (d + 1)
        S_running.add(S[d])
        T_running.add(T[d])

    rbo_score = AO[-1] + A[-1] * p**k if ext and p < 1 else AO[-1]
    return max(0.0, min(1.0, rbo_score))


def gwets_ac1(S, T):
    """
    Compute Gwet's AC1 inter-rater agreement coefficient.

    Args:
        S (list or np.ndarray): Ratings from the first rater.
        T (list or np.ndarray): Ratings from the second rater.

    Returns:
        float: Gwet's AC1 coefficient.
    """
    rater1, rater2 = np.array(S), np.array(T)
    assert len(rater1) == len(rater2), "Both raters must have the same number of ratings."

    unique_labels = np.unique(np.concatenate((rater1, rater2)))

    # Compute observed agreement (Po)
    Po = np.mean(rater1 == rater2)

    # Compute expected agreement (Pe)
    label_probs = {label: (np.sum(rater1 == label) + np.sum(rater2 == label)) / (2 * len(rater1)) for label in unique_labels}
    Pe = sum(p**2 for p in label_probs.values())

    # Compute Gwet's AC1
    if Pe == 1:
        return 1.0  # Perfect agreement

    AC1 = (Po - Pe) / (1 - Pe)
    return AC1
