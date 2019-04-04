"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


import pandas as pd
import numpy as np


def contingency_table(f1, f2, O11, N):
    """
    Calculate contingency table for observed data.
    f1 = R1 = O11 + O12 (Anzahl Vorkommen von t1)
    f2 = C1 = O11 + O21 (Anzahl Vorkommen von t2)
    O11 = O (Anzahl gemeinsame Vorkommen von t1 und t2)
    N: Number of tokens in corpus
    :return: Tuple of pandas.Series
    :rtype: tuple
    """

    O12 = pd.Series(data=f1 - O11)
    O21 = pd.Series(f2 - O11)
    O22 = pd.Series(N - (f1 + f2 + O11))

    return (O12, O21, O22)


def expected_frequencies(f1, f2, N):
    """
    Calculate expected frequencies for observed frequencies.
    """

    E11 = (f1 * f2) / N

    return pd.Series(data=E11)


def z_score(row):
    """
    Calculate z-score
    """
    if 'E11' not in row.index:
        return np.nan
    return (row['O11'] - row['E11']) / np.sqrt(row['E11'])


def mutual_information(row):
    """
    Calculate Mutual Information
    """
    if 'E11' not in row.index:
        return np.nan
    return np.log2(row['O11'] / row['E11'])
