"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


from statistics import NormalDist  # requires python version >= 3.8
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


def log_likelihood(df, signed=True):
    """
    Calculate log-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22, E11, E12, E21, E22
    :param bool signed: return negative values for rows with O11 < E11?
    :return: log-likelihood
    :rtype: pd.Series
    """

    ii = phi(df['O11'], df['E11'])
    ij = phi(df['O12'], df['E12'])
    ji = phi(df['O21'], df['E21'])
    jj = phi(df['O22'], df['E22'])

    am = 2 * (ii + ij + ji + jj)

    if signed:
        am = np.sign(df['O11'] - df['E11']) * am

    return am


def hypergeometric_likelihood(df):
    """
    Calculate hypergeometric-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :return: hypergeometric-likelihood
    :rtype: pd.Series
    """

    df = df.astype(
        {'O11': 'int32', 'O12': 'int32', 'O21': 'int32', 'O22': 'int32'}
    )

    np.seterr(all='ignore')
    c1 = CHOOSE(df['O11'] + df['O21'], df['O11'])
    c2 = CHOOSE(df['O12'] + df['O22'], df['O12'])
    c3 = CHOOSE(df['O11'] + df['O12'] + df['O21'] + df['O22'], df['O11'] + df['O12'])
    am = c1 / c3 * c2
    np.seterr(all='warn')

    return am


def binomial_likelihood(df):
    """
    Calculate binomial-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22, E11
    :return: binomial-likelihood
    :rtype: pd.Series
    """

    df = df.astype(
        {'O11': 'int32', 'O12': 'int32', 'O21': 'int32', 'O22': 'int32'}
    )

    N = df['O11'] + df['O12'] + df['O21'] + df['O22']

    np.seterr(all='ignore')
    c1 = CHOOSE(N, df['O11'])
    c2 = (df['E11'] / N) ** df['O11']
    c3 = (1 - df['E11'] / N) ** (N - df['O11'])
    am = c1 * c2 * c3
    np.seterr(all='warn')

    return am


def log_ratio(df, disc=.5):
    """
    Calculate log-ratio, a.k.a. relative risk

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :return: log-ratio
    :rtype: pd.Series
    """

    # questionable discounting according to Hardie (2014)
    O21_disc = df['O21'].where(df['O21'] != 0, disc)

    R1 = df['O11'] + df['O12']
    R2 = df['O21'] + df['O22']

    am = np.log2((df['O11'] / O21_disc) / (R1 / R2))

    return am


def conservative_log_ratio(df, alpha=.01, correct=True, disc=.5, one_sided=False):
    """
    Calculate conservative log-ratio, i.e. the binary logarithm of the
    lower bound of the confidence interval of relative risk at the
    (Bonferroni-corrected) confidence level.

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :return: conservative log-ratio
    :rtype: pd.Series

    """

    # questionable discounting according to Hardie (2014)
    O21_disc = df['O21'].where(df['O21'] != 0, disc)

    # compute natural logarithm of relative risk
    # so we can use estimate for standard error of log(RR)
    R1 = df['O11'] + df['O12']
    R2 = df['O21'] + df['O22']
    lrr = np.log((df['O11'] / O21_disc) / (R1 / R2))

    # Bonferroni correction
    if correct:
        vocab = (df['O11'] >= 1).sum()
        alpha /= vocab

    # get respective quantile of normal distribution
    if not one_sided:
        alpha /= 2
    z_factor = NormalDist().inv_cdf(1 - alpha)

    # asymptotic standard deviation of log(RR) according to Wikipedia
    R1 = df['O11'] + df['O12']
    R2 = df['O21'] + df['O22']
    lrr_sd = np.sqrt(1/df['O11'] + 1/O21_disc - 1/R1 - 1/R2)

    # calculate and apply appropriate boundary
    ci_min = (lrr - lrr_sd * z_factor).clip(lower=0)
    ci_max = (lrr + lrr_sd * z_factor).clip(upper=0)
    clrr = ci_min.where(lrr >= 0, ci_max)

    # adjust to binary logarithm
    clrr = clrr / np.log(2)

    return clrr


def list_measures():
    """ return a dictionary of implemented measures (name: measure)

    :return: dictionary of measures
    :rtype: dict
    """

    return {
        'z_score': z_score,
        't_score': t_score,
        'dice': dice,
        'log_likelihood': log_likelihood,
        'mutual_information': mutual_information,
        'log_ratio': log_ratio,
        'conservative_log_ratio': conservative_log_ratio
    }


def calculate_measures(df, measures=None, freq=False):
    """
    Calculate a list of association measures. Defaults to all available measures.

    :param pandas.DataFrame df: Dataframe with reasonably-named freq. signature
    :param list measures: names of AMs (or AMs)
    :param bool freq: return frequency signatures?

    :return: association measures
    :rtype: pandas.DataFrame
    """

    ams_all = list_measures()
    freq_columns = ['O11', 'O12', 'O21', 'O22', 'E11', 'E12', 'E21', 'E22']

    # take (or create) appropriate columns
    if not (df.columns.isin(freq_columns)).all():
        df_obs = observed_frequencies(df)
        df_exp = expected_frequencies(df)
        df = df_obs.join(df_exp)
    df = df[freq_columns]

    # select measures
    if measures is not None:
        if isinstance(measures[0], str):
            measures = [ams_all[k] for k in measures if k in ams_all.keys()]
    else:
        measures = [ams_all[k] for k in ams_all]

    # calculate measures
    for measure in measures:
        df[measure.__name__] = measure(df)

    if not freq:
        df = df.drop(freq_columns, axis=1)

    return df
