"""comparison of ranked lists

RBO implementation based on https://github.com/dlukes/rbo

"""


import math


def set_at_depth(lst, depth):
    ans = set()
    for v in lst[:depth]:
        if isinstance(v, set):
            ans.update(v)
        else:
            ans.add(v)
    return ans


def raw_overlap(list1, list2, depth):
    """Overlap as defined in the article.

    """
    set1, set2 = set_at_depth(list1, depth), set_at_depth(list2, depth)
    return len(set1.intersection(set2)), len(set1), len(set2)


def overlap(list1, list2, depth):
    """Overlap which accounts for possible ties.

    This isn't mentioned in the paper but should be used in the ``rbo*()``
    functions below, otherwise overlap at a given depth might be > depth which
    inflates the result.

    There are no guidelines in the paper as to what's a good way to calculate
    this, but a good guess is agreement scaled by the minimum between the
    requested depth and the lengths of the considered lists (overlap shouldn't
    be larger than the number of ranks in the shorter list, otherwise results
    are conspicuously wrong when the lists are of unequal lengths -- rbo_ext is
    not between rbo_min and rbo_min + rbo_res.

    """
    return agreement(list1, list2, depth) * min(depth, len(list1), len(list2))
    # NOTE: comment the preceding and uncomment the following line if you want
    # to stick to the algorithm as defined by the paper
    # return raw_overlap(list1, list2, depth)[0]


def agreement(list1, list2, depth):
    """Proportion of shared values between two sorted lists at given depth.

    """
    len_intersection, len_set1, len_set2 = raw_overlap(list1, list2, depth)
    return 2 * len_intersection / (len_set1 + len_set2)


def save_log(x):
    return (x) if x != 0 else 0


def rbo_min(list1, list2, p, depth=None):
    """Tight lower bound on RBO.

    See equation (11) in paper.

    """
    depth = min(len(list1), len(list2)) if depth is None else depth
    x_k = overlap(list1, list2, depth)
    log_term = x_k * math.log(1 - p)
    sum_term = sum(
        p ** d / d * (overlap(list1, list2, d) - x_k) for d in range(1, depth + 1)
    )
    return (1 - p) / p * (sum_term - log_term)


def rbo_res(list1, list2, p):
    """Upper bound on residual overlap beyond evaluated depth.

    See equation (30) in paper.

    """
    shorter, longer = sorted((list1, list2), key=len)
    length_s, length_l = len(shorter), len(longer)
    x_l = overlap(list1, list2, length_l)
    # since overlap(...) can be fractional in the general case of ties and f
    # must be an integer --> math.ceil()
    f = int(math.ceil(length_l + length_s - x_l))
    # upper bound of range() is non-inclusive, therefore + 1 is needed
    term1 = length_s * sum(p ** d / d for d in range(length_s + 1, f + 1))
    term2 = length_l * sum(p ** d / d for d in range(length_l + 1, f + 1))
    term3 = x_l * (math.log(1 / (1 - p)) - sum(p ** d / d for d in range(1, f + 1)))
    return p ** length_s + p ** length_l - p ** f - (1 - p) / p * (term1 + term2 + term3)


def rbo_ext(list1, list2, p):
    """RBO point estimate based on extrapolating observed overlap.

    See equation (32) in paper.

    """
    shorter, longer = sorted((list1, list2), key=len)
    length_s, length_l = len(shorter), len(longer)
    x_l = overlap(list1, list2, length_l)
    x_s = overlap(list1, list2, length_s)
    # the paper says overlap(..., d) / d, but it should be replaced by
    # agreement(..., d) defined as per equation (28) so that ties are handled
    # properly (otherwise values > 1 will be returned)
    # sum1 = sum(p**d * overlap(list1, list2, d)[0] / d for d in range(1, l + 1))
    sum1 = sum(p ** d * agreement(list1, list2, d) for d in range(1, length_l + 1))
    sum2 = sum(p ** d * x_s * (d - length_s) / length_s / d for d in range(length_s + 1, length_l + 1))
    term1 = (1 - p) / p * (sum1 + sum2)
    term2 = p ** length_l * ((x_l - x_s) / length_l + x_s / length_s)
    return term1 + term2


def rbo(list1, list2, p, k=None):
    """Complete RBO analysis (lower bound, residual, point estimate).

    ``list`` arguments should be already correctly sorted iterables and each
    item should either be an atomic value or a set of values tied for that
    rank. ``p`` is the probability of looking for overlap at rank k + 1 after
    having examined rank k.

    """

    if not 0 < p < 1:
        raise ValueError("The ``p`` parameter must be between 0 and 1.")

    if len(set(list1).intersection(set(list2))) == 0:
        return 0.0, 0.0, 0.0

    depth = k if k else min(len(list1), len(list2))
    list1 = list1[:min(len(list1), depth)]
    list2 = list2[:min(len(list2), depth)]

    args = (list1, list2, p)

    return rbo_min(*args), rbo_res(*args), rbo_ext(*args)


def contingency(left, right, candidates):

    left = set(left)
    right = set(right)

    a = len(left.intersection(right))
    b = len(left - right)
    c = len(right - left)
    d = len(candidates - left - right)

    return a, b, c, d


def cohens_kappa(left, right, candidates=None):
    """Compute Cohen's kappa between to ranked lists left and right.

    Args:
        left (list or np.ndarray): First ranked list.
        right (list or np.ndarray): Second ranked list.
        candidates (list or np.ndarray): Superset of left and right.

    Returns:
        float: Cohen's kappa.
    """
    if candidates is None:
        candidates = set(left).union(set(right))
    a, b, c, d = contingency(left, right, candidates)
    N = a + b + c + d
    if N == 0:
        return None  # avoid division by zero

    ao = (a + d) / N

    ae = 1 / (N ** 2) * ((a+c) * (a+b) + (b+d) * (c+d))

    kappa = (ao - ae) / (1 - ae)

    return kappa


def gwets_ac1(left, right, candidates=None):
    """Compute Gwet's AC1 inter-rater agreement coefficient between to ranked lists left and right.

    Args:
        left (list or np.ndarray): First ranked list.
        right (list or np.ndarray): Second ranked list.
        candidates (list or np.ndarray): Superset of left and right.

    Returns:
        float: Gwet's AC1 coefficient.
    """
    if candidates is None:
        candidates = set(left).union(set(right))
    a, b, c, d = contingency(left, right, candidates)
    N = a + b + c + d
    if N == 0:
        return None  # avoid division by zero

    ao = (a + d) / N
    q = 1 / 2 / N * (a + c + a + d)
    ae = 2 * q * (1 - q)

    if ae == 1:
        return None  # avoid division by zero in denominator

    ac1 = (ao - ae) / (1 - ae)

    return ac1
