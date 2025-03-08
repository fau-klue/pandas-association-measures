"""comparison of ranked lists

RBO implementation based on https://github.com/changyaochen/rbo/blob/master/rbo/rbo.py

"""

import numpy as np


def rbo(left, right, k=None, p=.95, ext=True):
    """
    Compute Rank-Biased Overlap (RBO) between two ranked lists left and right.

    Args:
        left (list or np.ndarray): First ranked list.
        right (list or np.ndarray): Second ranked list.
        k (int, optional): Depth of evaluation. Defaults to min(len(left), len(right)).
        p (float, optional): Weight parameter (0 < p < 1). Defaults to .95.
        ext (bool, optional): Whether to extrapolate RBO. Defaults to True.

    Returns:
        float: Rank-Biased Overlap (RBO) score.
    """
    if not left and not right:
        return 1.0  # Both lists are empty

    if not left or not right:
        return 0.0  # One list is empty

    if k is None:
        k = min(len(left), len(right))
    k = min(len(left), len(right), k)

    if p <= 0 or p > 1:
        raise ValueError("p must be between 0 (exclusive) and 1")

    # Initialize agreement and average overlap arrays
    a, ao = [0] * k, [0] * k
    weights = [1.0 * (1 - p) * p**d for d in range(k)] if p != 1.0 else [1.0] * k

    left_running, right_running = {left[0]}, {right[0]}
    a[0] = 1 if left[0] == right[0] else 0
    ao[0] = weights[0] * a[0] if p != 1.0 else a[0]

    for d in range(1, k):
        overlap = int(left[d] in right_running) + int(right[d] in left_running) + int(left[d] == right[d])
        a[d] = ((a[d - 1] * d) + overlap) / (d + 1)
        ao[d] = ao[d - 1] + weights[d] * ao[d] if p != 1.0 else ((ao[d - 1] * d) + a[d]) / (d + 1)
        left_running.add(left[d])
        right_running.add(right[d])

    rbo_score = ao[-1] + a[-1] * p**k if ext and p < 1 else ao[-1]
    return max(0.0, min(1.0, rbo_score))


def gwets_ac1(left, right):
    """
    Compute Gwet's AC1 inter-rater agreement coefficient between to ranked lists left and right.

    Args:
        left (list or np.ndarray): First ranked list.
        right (list or np.ndarray): Second ranked list.

    Returns:
        float: Gwet's AC1 coefficient.
    """

    left, right = np.array(left), np.array(right)
    if len(left) != len(right):
        raise ValueError("Both lists must have the same number of items.")

    unique_labels = np.unique(np.concatenate((left, right)))

    # Compute observed agreement
    ao = np.mean(left == right)

    # Compute expected agreement
    label_probs = {label: (np.sum(left == label) + np.sum(right == label)) / (2 * len(left)) for label in unique_labels}
    ae = sum(p**2 for p in label_probs.values())

    # Compute Gwet's AC1
    if ae == 1:
        return 1.0  # Perfect agreement

    ac1 = (ao - ae) / (1 - ae)
    return ac1
