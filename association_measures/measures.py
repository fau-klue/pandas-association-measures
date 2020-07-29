"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


import numpy as np
from .binomial import choose
from .frequencies import expected_frequencies, observed_frequencies


CHOOSE = np.vectorize(choose)


def phi(o, e):
    """
    Calculate phi(o,e):=o*log(o/e) with lim_{o↓0} phi(o,e)=0

    :param Series o: pd.Series of observed frequencies
    :param Series e: pd.Series of expected frequencies
    :return: phi
    :rtype: pd.Series
    """

    np.seterr(divide='ignore')

    values = o * np.log(o / e)
    values[values.isna()] = 0    # NaNs where o=0 → phi=0

    np.seterr(divide='warn')

    return values


def z_score(df):
    """
    Calculate z-score

    :param DataFrame df: pd.DataFrame with columns O11 and E11
    :return: z-score
    :rtype: pd.Series
    """
    am = (df['O11'] - df['E11']) / np.sqrt(df['E11'])
    return am


def t_score(df):
    """
    Calculate t-score

    :param DataFrame df: pd.DataFrame with columns O11 and E11
    :return: t-score
    :rtype: pd.Series
    """

    am = (df['O11'] - df['E11']) / np.sqrt(df['O11'])
    return am


def mutual_information(df):
    """
    Calculate Mutual Information

    :param DataFrame df: pd.DataFrame with columns O11 and E11
    :return: mutual information
    :rtype: pd.Series
    """

    am = np.log10(df['O11'] / df['E11'])

    return am


def dice(df):
    """
    Calculate Dice coefficient

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21
    :return: dice
    :rtype: pd.Series
    """

    am = (2 * df['O11']) / (2 * df['O11'] + df['O12'] + df['O21'])

    return am


def log_likelihood(df):
    """
    Calculate log-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22, E11, E12, E21, E22
    :return: log-likelihood
    :rtype: pd.Series
    """

    ii = phi(df['O11'], df['E11'])
    ij = phi(df['O12'], df['E12'])
    ji = phi(df['O21'], df['E21'])
    jj = phi(df['O22'], df['E22'])

    am = 2 * (ii + ij + ji + jj)

    # calculate signed version by default
    am = np.sign(df['O11'] - df['E11']) * am

    return am


def hypergeometric_likelihood(df):
    """
    Calculate hypergeometric-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :return: hypergeometric likelihood
    :rtype: pd.Series
    """

    c1 = CHOOSE(df['O11'] + df['O21'], df['O11'])
    c2 = CHOOSE(df['O12'] + df['O22'], df['O12'])
    c3 = CHOOSE(df['O11'] + df['O12'] + df['O21'] + df['O22'], df['O11'] + df['O12'])

    am = c1 * c2 / c3

    return am


def log_ratio(df):
    """
    Calculate log-ratio

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :return: log-ratio
    :rtype: pd.Series
    """

    C1 = df['O11'] + df['O21']
    C2 = df['O12'] + df['O22']
    am = np.log2((df['O11'] / C1) / (df['O12'] / C2))

    return am


def calculate_measures(df, measures=None):
    """
    Calculate a list of association measures. Defaults to all available measures.

    :param pandas.DataFrame df: Dataframe with reasonably-named freq. signature
    :param measures list: names of AMs (or AMs)
    :return: pandas.DataFrame with association measures
    :rtype: pandas.DataFrame
    """

    # implemented measures
    ams_all = {
        'z_score': z_score,
        't_score': t_score,
        'dice': dice,
        'log_likelihood': log_likelihood,
        'mutual_information': mutual_information,
        'log_ratio': log_ratio,
    }

    # take (or create) appropriate columns
    if not (df.columns.isin(
            ['O11', 'O12', 'O21', 'O22', 'E11', 'E12', 'E21', 'E22']
    ).all()):
        df_obs = observed_frequencies(df)
        df_exp = expected_frequencies(df)
        df = df_obs.join(df_exp)

    df = df[['O11', 'O12', 'O21', 'O22', 'E11', 'E12', 'E21', 'E22']]

    # select measures
    if measures is not None:
        if isinstance(measures[0], str):
            measures = [ams_all[k] for k in measures if k in ams_all.keys()]
    else:
        measures = [ams_all[k] for k in ams_all]

    # calculate measures
    for measure in measures:
        df[measure.__name__] = measure(df)

    df = df.drop(['O11', 'O12', 'O21', 'O22', 'E11', 'E12', 'E21', 'E22'], axis=1)

    return df
