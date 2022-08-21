"""
observed (O11, O12, O21, O22) and expected (E11, E12, E21, E22) frequencies

"""

from pandas import DataFrame


def observed_frequencies(df, f1=None, N=None, N1=None, N2=None, marginals=False):
    """Return observed frequencies in contingency table notation
    (O11..O22). Raises a Value Error if columns are not reasonably
    named.

    Notation for marginals (Evert 2008):
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

    Integers can also be passed as scalar arguments.

    :param DataFrame df: DataFrame with reasonably-named frequency columns
    :param bool marginals: add marginals? (R1, R2, C1, C2, N)
    :return: df with same index and columns O11, O12, O21, O22
    :rtype: DataFrame

    """

    # integer parameters instead of columns?
    if all(v is None for v in [f1, N1, N2, N]):
        pass

    elif f1 is not None and N is not None:
        try:
            df = df[['f', 'f2']].copy()
            df['f1'] = f1
            df['N'] = N
        except KeyError:
            raise ValueError(
                'frequency signature notation: (f1, N) are given, but (f, f2) are not'
            )

    elif N1 is not None and N2 is not None:
        try:
            df = df[['f1', 'f2']].copy()
            df['N1'] = N1
            df['N2'] = N2
        except KeyError:
            raise ValueError(
                'corpus frequency notation: (N1, N2) are given, but (f1, f2) are not'
            )

    else:
        raise ValueError(
            'either (f1, N) OR (N1, N2) have to be given'
        )

    # already in contingency notation?
    if set(['O11', 'O12', 'O21', 'O22']).issubset(df.columns):
        O11 = df['O11']
        O12 = df['O12']
        O21 = df['O21']
        O22 = df['O22']

    # frequency signature:
    elif set(['f', 'f1', 'f2', 'N']).issubset(df.columns):
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

    # construct dataframe
    obs = DataFrame(
        index=df.index,
        data={
            'O11': O11,
            'O12': O12,
            'O21': O21,
            'O22': O22
        }
    )

    # add marginals
    if marginals:
        obs['R1'] = obs['O11'] + obs['O12']
        obs['R2'] = obs['O21'] + obs['O22']
        obs['C1'] = obs['O11'] + obs['O21']
        obs['C2'] = obs['O12'] + obs['O22']
        obs['N'] = obs['R1'] + obs['R2']

    return obs


def expected_frequencies(df, observed=False):
    """Calculate expected frequencies for observed frequencies assuming
    independence.

    :param pandas.DataFrame df: df with reasonably named columns
    :param bool observed: also return observed frequencies (contingency notations, incl. marginals)
    :return: df with same index and columns E11, E12, E21, E22
    :rtype: pandas.DataFrame

    """

    # convert input if necessary
    obs = observed_frequencies(df, marginals=True)

    # expected frequencies
    E11 = (obs['R1'] * obs['C1']) / obs['N']
    E12 = (obs['R1'] * obs['C2']) / obs['N']
    E21 = (obs['R2'] * obs['C1']) / obs['N']
    E22 = (obs['R2'] * obs['C2']) / obs['N']

    # construct dataframe
    expected = DataFrame(
        index=df.index,
        data={
            'E11': E11,
            'E12': E12,
            'E21': E21,
            'E22': E22
        }
    )

    # return marginals?
    df = obs.join(expected) if observed else expected

    return df
