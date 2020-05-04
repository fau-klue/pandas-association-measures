"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


import numpy as np
from .binomial import choose
from .frequencies import expected_frequencies, observed_frequencies


def phi(o, e):
    """
    Calculate phi(o,e):=o*log(o/e) with lim_{o↓0} phi(o,e)=0

    :param int o: observed frequency
    :param float e: expected frequency
    :return: phi
    :rtype: float
    """

    if o == 0:
        return 0
    elif e == 0:
        raise ValueError("observed value must be 0 if expected value is zero")
    else:
        return o * np.log(o / e)


def z_score(freq):
    """
    Calculate z-score

    :param dict freq: dictionary-like object with O11 and E11
    :return: z-score
    :rtype: float
    """

    am = (freq['O11'] - freq['E11']) / np.sqrt(freq['E11'])

    return am


def t_score(freq):
    """
    Calculate t-score

    :param dict freq: dictionary-like object with O11 and E11
    :return: t-score
    :rtype: float
    """

    am = (freq['O11'] - freq['E11']) / np.sqrt(freq['O11'])

    return am


def mutual_information(freq):
    """
    Calculate Mutual Information

    :param dict freq: dictionary-like object with O11 and E11
    :return: mutual_information
    :rtype: float
    """

    am = np.log10(freq['O11'] / freq['E11'])

    return am


def dice(freq):
    """
    Calculate Dice coefficient

    :param dict freq: dictionary-like object with O11, O12, O21
    :return: dice
    :rtype: float
    """

    am = (2 * freq['O11']) / (2 * freq['O11'] + freq['O12'] + freq['O21'])

    return am


def log_likelihood(freq, signed=True):
    """
    Calculate log-likelihood

    :param dict freq: dictionary-like object with O11, O12, O21, O22, E11, E12, E21, E22
    :param bool signed: whether to return negative values for anti-collocates
    :return: log-likelihood
    :rtype: float
    """

    ii = phi(freq['O11'], freq['E11'])
    ij = phi(freq['O12'], freq['E12'])
    ji = phi(freq['O21'], freq['E21'])
    jj = phi(freq['O22'], freq['E22'])

    am = 2 * (ii + ij + ji + jj)
    if signed:
        am = np.sign(freq['O11'] - freq['E11']) * am

    return am


def hypergeometric_likelihood(freq):
    """
    Calculate hypergeometric-likelihood

    :param dict freq: dictionary-like object with O11, O12, O21, O22
    :return: dice
    :rtype: float
    """

    N = freq['O11'] + freq['O12'] + freq['O21'] + freq['O22']
    if N == 0:
        return np.nan
    am = (
        choose(freq['O11'] + freq['O21'], freq['O11']) *
        choose(freq['O12'] + freq['O22'], freq['O12'])
    ) / choose(N, freq['O11'] + freq['O12'])
    return am


def log_ratio(freq):
    """
    Calculate log-ratio

    :param dict freq: dictionary-like object with O11, O12, O21, O22
    :return: log-ratio
    :rtype: float
    """

    C1 = freq['O11'] + freq['O21']
    C2 = freq['O12'] + freq['O22']
    am = np.log2(freq['O11'] / C1 / (freq['O12'] / C2))

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
        'hypergeometric_likelihood': hypergeometric_likelihood
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
        if type(measures[0]) == str:
            measures = [ams_all[k] for k in measures if k in ams_all.keys()]
    else:
        measures = [ams_all[k] for k in ams_all.keys() if k != 'hypergeometric_likelihood']

    # calculate measures
    for measure in measures:
        df[measure.__name__] = df.apply(measure, axis=1)

    df = df.drop(['O11', 'O12', 'O21', 'O22', 'E11', 'E12', 'E21', 'E22'], axis=1)

    return df
