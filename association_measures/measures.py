"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


# from statistics import NormalDist  # requires python version >= 3.8
from scipy.stats import norm       # requires scipy
import numpy as np

from .binomial import choose
from .frequencies import expected_frequencies, observed_frequencies


CHOOSE = np.vectorize(choose)


def list_measures():
    """
    Return a dictionary of implemented measures (name: measure)

    :return: dictionary of measures
    :rtype: dict
    """

    return {
        # asymptotic hypothesis tests
        'z_score': z_score,
        't_score': t_score,
        'log_likelihood': log_likelihood,
        'simple_ll': simple_ll,
        # point estimates of association strength
        'dice': dice,
        'log_ratio': log_ratio,
        # likelihood measures
        # 'hypergeometric_likelihood': hypergeometric_likelihood,
        # 'binomial_likelihood': binomial_likelihood,
        # information theory
        'mutual_information': mutual_information,
        'local_mutual_information': local_mutual_information,
        # conservative estimates
        'conservative_log_ratio': conservative_log_ratio
    }


def calculate_measures(df, measures=None, freq=False):
    """
    Calculate a list of association measures. Defaults to all available
    (and numerically stable) measures.

    :param pandas.DataFrame df: Dataframe with reasonably-named freq. signature
    :param list measures: names of AMs (or AMs)
    :param bool freq: also return frequency signatures?

    :return: association measures
    :rtype: pandas.DataFrame
    """

    # take (or create) appropriate columns
    freq_columns = ['O11', 'O12', 'O21', 'O22', 'E11', 'E12', 'E21', 'E22']
    if not set(freq_columns).issubset(set(df.columns)):
        df_obs = observed_frequencies(df)
        df_exp = expected_frequencies(df)
        df = df_obs.join(df_exp)
    else:
        df = df[freq_columns].copy()

    # select measures
    ams_all = list_measures()
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


###############################
# ASYMPTOTIC HYPOTHESIS TESTS #
###############################

def z_score(df):
    """
    Calculate z-score

    :param DataFrame df: DataFrame with columns O11 and E11
    :return: z-score
    :rtype: pd.Series
    """

    am = (df['O11'] - df['E11']) / np.sqrt(df['E11'])

    return am


def t_score(df, disc=.001):
    """
    Calculate t-score

    :param DataFrame df: pd.DataFrame with columns O11 and E11
    :param float disc: discounting (or smoothing) parameter for O11 == 0
    :return: t-score
    :rtype: pd.Series
    """

    O11_disc = df['O11'].where(df['O11'] != 0, disc)
    am = (df['O11'] - df['E11']) / np.sqrt(O11_disc)

    return am


def log_likelihood(df, signed=True):
    """
    Calculate log-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22, E11, E12, E21, E22
    :param bool signed: return negative values for rows with O11 < E11?
    :return: log-likelihood
    :rtype: pd.Series
    """

    # NB: discounting will not have any effect since term will be multiplied by original Oij = 0
    O11_disc = df['O11'].where(df['O11'] != 0, 1)
    O12_disc = df['O12'].where(df['O12'] != 0, 1)
    O21_disc = df['O21'].where(df['O21'] != 0, 1)
    O22_disc = df['O22'].where(df['O22'] != 0, 1)

    ii = df['O11'] * np.log(O11_disc / df['E11'])
    ij = df['O12'] * np.log(O12_disc / df['E12'])
    ji = df['O21'] * np.log(O21_disc / df['E21'])
    jj = df['O22'] * np.log(O22_disc / df['E22'])

    am = 2 * (ii + ij + ji + jj)

    if signed:
        am = np.sign(df['O11'] - df['E11']) * am

    return am


def simple_ll(df, signed=True):
    """
    Calculate simple log-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, E11
    :param bool signed: return negative values for rows with O11 < E11?
    :return: simple log-likelihood
    :rtype: pd.Series
    """

    # NB: discounting will not have any effect since term will be multiplied by original O11 = 0
    O11_disc = df['O11'].where(df['O11'] != 0, 1)

    log_term = df['O11'] * np.log(O11_disc / df['E11'])

    am = 2 * (log_term - (df['O11'] - df['E11']))

    if signed:
        am = np.sign(df['O11'] - df['E11']) * am

    return am


###########################################
# POINT ESTIMATES OF ASSOCIATION STRENGTH #
###########################################

def dice(df):
    """
    Calculate Dice coefficient

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21
    :return: dice
    :rtype: pd.Series
    """

    am = (2 * df['O11']) / (2 * df['O11'] + df['O12'] + df['O21'])

    return am


def log_ratio(df, disc=.5):
    """
    Calculate log-ratio, a.k.a. relative risk

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :param float disc: discounting (or smoothing) parameter for O11 == 0 and O21 == 0
    :return: log-ratio
    :rtype: pd.Series
    """

    # questionable discounting according to Hardie (2014)
    O11_disc = df['O11'].where(df['O11'] != 0, disc)
    O21_disc = df['O21'].where(df['O21'] != 0, disc)

    R1 = df['O11'] + df['O12']
    R2 = df['O21'] + df['O22']

    am = np.log2((O11_disc / O21_disc) / (R1 / R2))

    return am


#######################
# LIKELIHOOD MEASURES #
#######################

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
        {'O11': 'int32', 'O12': 'int32', 'O21': 'int32', 'O22': 'int32', 'E11': 'int32'}
    )

    N = df['O11'] + df['O12'] + df['O21'] + df['O22']

    np.seterr(all='ignore')
    c1 = CHOOSE(N, df['O11'])
    c2 = (df['E11'] / N) ** df['O11']
    c3 = (1 - df['E11'] / N) ** (N - df['O11'])
    am = c1 * c2 * c3
    np.seterr(all='warn')

    return am


##########################
# CONSERVATIVE ESTIMATES #
##########################

def conservative_log_ratio(df, alpha=.01, correct='Bonferroni', disc=.5, one_sided=False):
    """
    Calculate conservative log-ratio, i.e. the binary logarithm of the
    lower bound of the confidence interval of relative risk at the
    (Bonferroni-corrected) confidence level.

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :param float alpha: significance level
    :param str correct: correction type for several tests (None | "Bonferroni" | "Sidak")
    :param float disc: discounting (or smoothing) parameter for O11 == 0 and O21 == 0
    :param bool one_sided: calculate one- or two-sided confidence interval

    :return: conservative log-ratio
    :rtype: pd.Series

    """

    # questionable discounting according to Hardie (2014)
    O11_disc = df['O11'].where(df['O11'] != 0, disc)
    O21_disc = df['O21'].where(df['O21'] != 0, disc)

    # compute natural logarithm of relative risk
    # so we can use estimate for standard error of log(RR)
    R1 = df['O11'] + df['O12']
    R2 = df['O21'] + df['O22']
    lrr = np.log((O11_disc / O21_disc) / (R1 / R2))

    # Bonferroni or Sidak correction
    if isinstance(correct, str):
        vocab = (df['O11'] >= 1).sum()
        if correct == 'Bonferroni':
            alpha /= vocab
        elif correct == "Sidak":
            alpha = 1 - (1 - alpha) ** (1 / vocab)
        else:
            raise ValueError('parameter "correct" should either be "Bonferroni" or "Sidak".')
    elif correct is None:
        pass
    else:
        raise ValueError('parameter "correct" should either be None or a string.')

    # get respective quantile of normal distribution
    if not one_sided:
        alpha /= 2
    # z_factor = NormalDist().inv_cdf(1 - alpha)
    z_factor = norm.ppf(1 - alpha)

    # asymptotic standard deviation of log(RR) according to Wikipedia
    lrr_sd = np.sqrt(1/O11_disc + 1/O21_disc - 1/R1 - 1/R2)

    # calculate and apply appropriate boundary
    ci_min = (lrr - lrr_sd * z_factor).clip(lower=0)
    ci_max = (lrr + lrr_sd * z_factor).clip(upper=0)
    clrr = ci_min.where(lrr >= 0, ci_max)

    # adjust to binary logarithm
    clrr /= np.log(2)

    return clrr


######################
# INFORMATION THEORY #
######################

def mutual_information(df, disc=.001):
    """
    Calculate Mutual Information

    :param DataFrame df: pd.DataFrame with columns O11 and E11
    :param float disc: discounting (or smoothing) parameter for O11 == 0
    :return: mutual information
    :rtype: pd.Series
    """

    O11_disc = df['O11'].where(df['O11'] != 0, disc)
    am = np.log10(O11_disc / df['E11'])

    return am


def local_mutual_information(df):
    """
    Calculate Local Mutual Information

    :param DataFrame df: pd.DataFrame with columns O11 and E11
    :return: mutual information
    :rtype: pd.Series
    """

    # NB: discouting will not have any effect since term will be multiplied by original O11 = 0
    O11_disc = df['O11'].where(df['O11'] != 0, 1)
    am = df['O11'] * np.log10(O11_disc / df['E11'])

    return am
