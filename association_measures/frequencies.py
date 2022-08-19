"""
observed (O11, O12, O21, O22) and expected (E11, E12, E21, E22) frequencies

"""

from pandas import DataFrame


def observed_frequencies(df):
    """Return observed frequencies in contingency table notation
    (O11..O22). Raises a Value Error if columns are not reasonably
    named.

    NB: notation for marginals:
    - rows: R1 = O11 + O12, R2 = O21 + O22
    - columns: C1 = O11 + O21, C2 = O12 + O22
    - size: N = O11 + O12 + O21 + O22 = R1 + R2 = C1 + C2

    Possible input formats:
    - frequency signature (cf. Evert 2008: Figure 8):
      f  = O11                    # co-occurrence freq. of token and node / freq. in corpus 1
      f1 =  R1 <int>              # number of tokens in W(node) / size of corpus 1
      f2 =  C1                    # marginal freq. of token / freq. in corpus 1 + 2
      N  =   N <int>              # size of corpus without nodes / size of corpus 1 + 2
    - corpus frequencies ("keyword friendly"):
      f1 = O11                    # number of occurrences in corpus 1
      f2 = O21                    # number of occurrences in corpus 2
      N1 =  R1 <int>              # size of corpus 1
      N2 =  R2 <int>              # size of corpus 2

    :param DataFrame df: DataFrame with reasonably-named frequency columns
    :return: df with same index and columns O11, O12, O21, O22
    :rtype: DataFrame

    """

    # already in contingency notation?
    try:
        return df[['O11', 'O12', 'O21', 'O22']].copy()
    except KeyError:
        # well, it was worth a try
        pass

    # frequency signature:
    if set(['f', 'f1', 'f2', 'N']).issubset(df.columns):
        O11 = df['f']
        O12 = df['f1'] - O11
        O21 = df['f2'] - O11
        O22 = df['N'] - O11 - O12 - O21

    # corpus frequencies:
    elif set(['f1', 'N1', 'f2', 'N2']).issubset(df.columns):
        O11 = df['f1']
        O12 = df['N1'] - O11
        O21 = df['f2']
        O22 = df['N2'] - O21

    else:
        raise ValueError(f'columns are not reasonably named: {str(df.columns)}')

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

    # convert input if necessary
    obs = observed_frequencies(df)

    # marginal frequencies
    R1 = obs['O11'] + obs['O12']
    R2 = obs['O21'] + obs['O22']

    C1 = obs['O11'] + obs['O21']
    C2 = obs['O12'] + obs['O22']

    N = R1 + R2

    # expected frequencies
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
