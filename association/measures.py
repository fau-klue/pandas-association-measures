"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


import pandas as pd
import numpy as np


def contingency_table(df):
    """
    Calculate contingency table for observed data.
    f1 = R1 = O11 + O12 (Anzahl Vorkommen von t1)
    f2 = C1 = O11 + O21 (Anzahl Vorkommen von t2)
    O11 = O (Anzahl gemeinsame Vorkommen von t1 und t2)
    N: Number of tokens in corpus
    :return: Tuple of pandas.Series
    :rtype: tuple
    """

    O12 = pd.Series(data=df['f1'] - df['O11'])
    O21 = pd.Series(data=df['f2'] - df['O11'])
    O22 = pd.Series(data=df['N'] - (df['f1'] + df['f2'] + df['O11']))

    return (df['O11'], O12, O21, O22)


def expected_frequencies(df):
    """
    Calculate expected frequencies for observed frequencies.
    """

    if 'O12' not in df.columns:
        df['O11'], df['O12'], df['O21'], df['O22'] =contingency_table(df)

    R1 = df['f1'] # f1 Frequency
    C1 = df['f2'] # f2 Frequency
    R2 = df['O21'] + df['O22']
    C2 = df['O12'] + df['O22']

    E11 = (R1 * C1) / df['N']
    E12 = (R1 * C2) / df['N']
    E21 = (R2 * C1) / df['N']
    E22 = (R2 * C2) / df['N']

    return (E11, E12, E21, E22)


def z_score(df):
    """
    Calculate z-score
    """

    if 'E11' not in df.columns:
        return np.nan

    res = (df['O11'] - df['E11']) / np.sqrt(df['E11'])

    return pd.Series(data=res)


def mutual_information(df):
    """
    Calculate Mutual Information
    """

    if 'E11' not in df.columns:
        return np.nan

    res = np.log2(df['O11'] / df['E11'])

    return pd.Series(data=res)
