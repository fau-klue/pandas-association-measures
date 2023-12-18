from itertools import product

from numpy import exp, linspace, log
from pandas import DataFrame

from .measures import score


def expand_grid(dictionary):
    """Create a grid of all value combinations of all keys of the dictionary

    """

    return DataFrame([row for row in product(*dictionary.values())],
                     columns=dictionary.keys())


def log_seq(to=10e6, length=200, exact=50):
    """Create a logarithimcally scaled sequence

    """

    if length <= exact:
        raise ValueError()

    length = length - exact

    return list(range(exact + 1)) + [int(exp(s)) for s in sorted([x for x in linspace(log(exact), log(to), length)])]


def log_grid(N1=10e6, N2=10e6, length1=200, length2=200, exact1=50, exact2=50):
    """Create a logarithmically-scaled grid

    """
    return expand_grid({
        'f1': log_seq(N1, length1, exact=exact1),
        'f2': log_seq(N2, length2, exact=exact2)
    }).drop_duplicates().reset_index(drop=True)


def topography(N1=10e6, N2=10e6, length=200, length1=None, length2=None, exact=50, exact1=None, exact2=None):
    """Create logarithmically scaled grid and calculcate scores

    """

    exact1 = exact if exact1 is None else exact1
    exact2 = exact if exact2 is None else exact2
    length1 = length if length1 is None else length1
    length2 = length if length2 is None else length2

    # support
    g = log_grid(N1=N1, N2=N2, length1=length1, length2=length2, exact1=exact1, exact2=exact2)

    # add scores
    scores = score(g, N1=N1, N2=N2)
    # .. add alternative for CLR
    scores['clr_normal'] = score(
        g, N1=N1, N2=N2, boundary='normal', measures=['conservative_log_ratio']
    )['conservative_log_ratio']
    # .. add alternative for log-ratio
    scores['log_ratio_hardie'] = score(
        g, N1=N1, N2=N2, discounting='Hardie2014', measures=['log_ratio']
    )['log_ratio']

    return scores
