"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


import pandas as pd
import numpy as np


def contingency_table(row):
    """
    Calculate contingency table for observed data.
    f1 = R1 = O11 + O12 (Anzahl Vorkommen von t1)
    f2 = C1 = O11 + O21 (Anzahl Vorkommen von t2)
    O11 = O (Anzahl gemeinsame Vorkommen von t1 und t2)
    N: Number of tokens in corpus
    :param pandas.Series row: Pandas Series containing f1, f2, O11 and N
    :return: pandas.Series containing O12, O21, O22
    :rtype: pandas.Series
    """

    # Way faster:
    # df['O12'] = df['f1'] - df['O11']
    # df['O21'] = df['f2'] - df['O11']
    # df['O22'] = df['N'] - (df['f1'] + df['f2'] + df['O11'])

    O12 = row['f1'] - row['O11']
    O21 = row['f2'] - row['O11']
    O22 = row['N'] - (row['f1'] + row['f2'] + row['O11'])
    return pd.Series([O12, O21, O22])


def expected_frequencies(row):
    """
    Calculate expected frequencies for observed frequencies.
    """
    # TODO: Should I do this in one step with the other data to avoid another iteration?
    # TODO: This is way faster: df['E11'] = (df['f1'] * df['f2']) / df['N']

    return (row['f1'] * row['f2']) / row['N']


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
