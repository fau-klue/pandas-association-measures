"""
Cooccurrence frequency data for a word pair (u,v) are often organised in a contingency table.

http://www.collocations.de/AM/index.html
"""


import pandas as pd


def observed_frequencies(df):
    """
    Calculate contingency table for observed data.

    f1 = R1 = O11 + O12 (marginal frequencies)
    f2 = C1 = O11 + O21 (marginal frequencies)
    O11 = joint frequency
    N: Number of tokens in corpus

    :param pandas.DataFrame df: Pandas Dataframe containing O11, f1, f2 and N
    :return: Tuple of pandas.Series containing observed frequencies for tokens
    :rtype: tuple
    """

    O12 = pd.Series(data=df['f1'] - df['O11'])
    O21 = pd.Series(data=df['f2'] - df['O11'])
    O22 = pd.Series(data=df['N'] - (df['O11'] + O12 + O21))

    return (df['O11'], O12, O21, O22)


def expected_frequencies(df):
    """
    Calculate expected frequencies for observed frequencies.

    :param pandas.DataFrame df: Pandas Dataframe containing O11, f1, f2 and N
    :return: Tuple of pandas.Series containing expected frequencies for tokens
    :rtype: tuple
    """

    if 'O12' not in df.columns:
        df['O11'], df['O12'], df['O21'], df['O22'] = observed_frequencies(df)

    R1 = df['f1'] # f1 Frequency
    C1 = df['f2'] # f2 Frequency
    R2 = df['O21'] + df['O22']
    C2 = df['O12'] + df['O22']

    E11 = (R1 * C1) / df['N']
    E12 = (R1 * C2) / df['N']
    E21 = (R2 * C1) / df['N']
    E22 = (R2 * C2) / df['N']

    return (E11, E12, E21, E22)
