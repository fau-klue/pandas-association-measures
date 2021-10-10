"""
observed (O11, O12, O21, O22) and expected (E11, E12, E21, E22) frequencies

http://www.collocations.de/AM/index.html
"""

from pandas import DataFrame


def observed_frequencies(df):
    """
    Calculate contingency table for observed data.

    naming conventions (cf. Evert 2008: Figure 8)
    f = O11                     # co-occurrence freq. of token and node
    f1 = R1 = O11 + O12         # number of tokens in W(node)
    f2 = C1 = O11 + O21         # marginal freq. of token
    N = O11 + O12 + O21 + O22   # size of corpus without nodes

    :param pandas.DataFrame df: df with O11|f, O12|f1, O21|f2, O22|N
    :return: df with same index and columns O11, O12, O21, O22
    :rtype: pandas.DataFrame
    """

    # check f / O11
    if 'O11' in df.columns:
        if 'f' in df.columns:
            if not df['O11'].equals(df['f']):
                raise ValueError(
                    'both "f" and "O11" are given but they are not the same'
                )
        O11 = df['O11']
    elif 'f' in df.columns:
        O11 = df['f']
    else:
        raise ValueError(
            'co-occurrence frequency must be given as column "f" or "O11"'
        )

    # check f1 / O12
    if 'O12' in df.columns:
        O12 = df['O12']
    elif 'f1' in df.columns:
        O12 = df['f1'] - O11
    else:
        raise ValueError('either "O12" or "f1" (= "R1") must be given')

    # check f2 / O21
    if 'O21' in df.columns:
        O21 = df['O21']
    elif 'f2' in df.columns:
        O21 = df['f2'] - O11
    else:
        raise ValueError('either "O21" or "f2" (= "C1") must be given')

    # check N / O22
    if 'O22' in df.columns:
        O22 = df['O22']
        # N = O11 + O12 + O21 + O22
    elif 'N' in df.columns:
        N = df['N']
        O22 = N - O11 - O12 - O21
    else:
        raise ValueError('either "O22" or "N" must be given')

    return DataFrame(
        index=df.index,
        data={
            'O11': O11,
            'O12': O12,
            'O21': O21,
            'O22': O22
        }
    )


def expected_frequencies(df):
    """
    Calculate expected frequencies for observed frequencies.

    :param pandas.DataFrame df: df with reasonably named columns
    :return: df with same index and columns E11, E12, E21, E22
    :rtype: pandas.DataFrame
    """

    if not df.columns.isin(['O11', 'O12', 'O21', 'O22']).all():
        obs = observed_frequencies(df)
    else:
        obs = df[['O11', 'O12', 'O21', 'O22']]

    R1 = obs['O11'] + obs['O12']
    R2 = obs['O21'] + obs['O22']
    C1 = obs['O11'] + obs['O21']
    C2 = obs['O12'] + obs['O22']
    N = R1 + R2

    E11 = (R1 * C1) / N
    E12 = (R1 * C2) / N
    E21 = (R2 * C1) / N
    E22 = (R2 * C2) / N

    return DataFrame(
        index=df.index,
        data={
            'E11': E11,
            'E12': E12,
            'E21': E21,
            'E22': E22
        }
    )
