"""
association measures

"""

import numpy as np
from pandas import concat
from scipy.stats import norm, beta
from warnings import warn

from .binomial import choose
from .frequencies import expected_frequencies, observed_frequencies


CHOOSE = np.vectorize(choose)


def list_measures():
    """Return a dictionary of implemented measures (name: measure)

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
        'min_sensitivity': min_sensitivity,
        'liddell': liddell,
        'dice': dice,
        'log_ratio': log_ratio,
        # likelihood measures
        # 'hypergeometric_likelihood': hypergeometric_likelihood,
        # 'binomial_likelihood': binomial_likelihood,
        # conservative estimates
        'conservative_log_ratio': conservative_log_ratio,
        # information theory
        'mutual_information': mutual_information,
        'local_mutual_information': local_mutual_information,
    }


def score(df, measures=None, f1=None, N=None, N1=None, N2=None,
          freq=True, per_million=True, digits=6, disc=.001,
          signed=True, alpha=.001, correct='Bonferroni',
          boundary='normal', vocab=None, one_sided=False):
    """Calculate a list of association measures on columns of df. Defaults
    to all available (and numerically stable) measures.

    Columns of df must follow one of the following notations:
    - contingency table: O11, O12, O21, O22
    - frequency signature: f, f1, f2, N
    - corpus frequencies: f1, N1, f2, N2
    Integers (f1, N, N1, N2) can also be passed as scalar arguments. See
    frequencies.observed_frequencies for further info on notation.

    :param DataFrame df: Dataframe with reasonably-named frequency columns
    :param list measures: names of measures (or measures)
    :param bool freq: also return observed and expected frequencies (incl. marginals)?
    :param bool per_million: return instances per million? (only if freq is True)
    :param int digits: round scores

    Further keyword arguments will be passed to the respective measures:
    :param float disc: discounting (or smoothing) parameter for O11 == 0 (and O21 == 0)
    :param bool signed: enforce negative values for rows with O11 < E11?
    :param float alpha: CLR: significance level
    :param str boundary: CLR: exact CI boundary of [poisson] distribution or [normal] approximation?
    :param str correct: CLR: correction type repeated tests (None|"Bonferroni"|"Sidak")
    :param int vocab: CLR: size of vocabulary (number of comparisons for correcting alpha)
    :param bool one_sided: CLR: calculate one- or two-sided confidence interval

    :return: association measures
    :rtype: DataFrame

    """

    # convert input to contingency notation and calculate expected frequencies
    df = observed_frequencies(df, f1=f1, N=N, N1=N1, N2=N2)
    df = expected_frequencies(df, observed=True)
    freq_columns = df.columns

    # select measures
    ams_all = list_measures()
    if measures is not None:
        if isinstance(measures[0], str):
            # TODO issue warning if measure not in list
            measures = [ams_all[k] for k in measures if k in ams_all.keys()]
    else:
        measures = [ams_all[k] for k in ams_all]

    # calculate measures
    for measure in measures:
        df[measure.__name__] = measure(
            df, disc=disc, signed=signed, alpha=alpha,
            correct=correct, boundary=boundary, vocab=vocab, one_sided=one_sided
        )

    # frequency columns?
    if not freq:
        df = df.drop(freq_columns, axis=1)
    else:
        # add instances (per million)
        fac = 10**6 if per_million else 1
        name = 'ipm' if per_million else 'instances'
        df[name] = df['O11'] / df['R1'] * fac
        df[name + '_reference'] = df['O21'] / df['R2'] * fac
        df[name + '_expected'] = df['E11'] / df['R1'] * fac

    # rounding
    df = round(df, digits) if digits is not None else df

    return df


def calculate_measures(df, measures=None, freq=False, per_million=True, digits=None, **kwargs):
    """deprecated since 0.2.3, use `score()` instead.

    """
    warn(
        "`calculate_measures()` is deprecated since version 0.2.3, use `score()` instead",
        DeprecationWarning,
        stacklevel=2
    )
    return score(df, measures=measures, freq=freq, per_million=per_million, digits=digits, **kwargs)


###############################
# ASYMPTOTIC HYPOTHESIS TESTS #
###############################

def z_score(df, **kwargs):
    """
    Calculate z-score

    :param DataFrame df: DataFrame with columns O11 and E11
    :return: z-score
    :rtype: pd.Series
    """

    am = (df['O11'] - df['E11']) / np.sqrt(df['E11'])

    return am


def t_score(df, disc=.001, **kwargs):
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


def log_likelihood(df, signed=True, **kwargs):
    """
    Calculate log-likelihood

    :param DataFrame df: pd.DataFrame with columns O11..O22, E11..E22
    :param bool signed: return negative values for rows with O11 < E11?
    :return: log-likelihood
    :rtype: pd.Series
    """

    # NB: discounting will not have any effect:
    #     term will be multiplied by original Oij = 0
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


def simple_ll(df, signed=True, **kwargs):
    """
    Calculate simple log-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, E11
    :param bool signed: return negative values for rows with O11 < E11?
    :return: simple log-likelihood
    :rtype: pd.Series
    """

    # NB: discounting will not have any effect:
    #     term will be multiplied by original Oij = 0
    O11_disc = df['O11'].where(df['O11'] != 0, 1)

    log_term = df['O11'] * np.log(O11_disc / df['E11'])

    am = 2 * (log_term - (df['O11'] - df['E11']))

    if signed:
        am = np.sign(df['O11'] - df['E11']) * am

    return am


###########################################
# POINT ESTIMATES OF ASSOCIATION STRENGTH #
###########################################

def min_sensitivity(df, **kwargs):
    """Calculate Minimum Sensitivity.

    :param DataFrame df: pd.DataFrame with columns O11, R1, C1
    :return: dice
    :rtype: pd.Series
    """

    am1 = df['O11'] / df['R1']
    am2 = df['O11'] / df['C1']
    am = concat([am1, am2], axis=1).min(axis=1)

    return am


def liddell(df, **kwargs):
    """Calculate Liddell

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22, C1, C2
    :return: liddell
    :rtype: pd.Series
    """

    am = (df['O11'] * df['O22'] - df['O12'] * df['O21']) / df['C1'] / df['C2']

    return am


def dice(df, **kwargs):
    """
    Calculate Dice coefficient

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21
    :return: dice
    :rtype: pd.Series
    """

    am = (2 * df['O11']) / (2 * df['O11'] + df['O12'] + df['O21'])

    return am


def log_ratio(df, disc=.5, **kwargs):
    """Calculate log-ratio, i.e. binary logarithm of relative risk

    :param DataFrame df: pd.DataFrame with columns O11, O21, R1, R2
    :param float disc: discounting (or smoothing) parameter for O11 == 0 and O21 == 0
    :return: log-ratio
    :rtype: pd.Series
    """

    # questionable discounting according to Hardie (2014)
    O11_disc = df['O11'].where(df['O11'] != 0, disc)
    O21_disc = df['O21'].where(df['O21'] != 0, disc)

    am = np.log2((O11_disc / O21_disc) / (df['R1'] / df['R2']))

    return am


#######################
# LIKELIHOOD MEASURES #
#######################

def hypergeometric_likelihood(df, **kwargs):
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


def binomial_likelihood(df, **kwargs):
    """
    Calculate binomial-likelihood

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22, E11, N
    :return: binomial-likelihood
    :rtype: pd.Series
    """

    df = df.astype(
        {'O11': 'int32', 'O12': 'int32', 'O21': 'int32', 'O22': 'int32', 'E11': 'int32'}
    )

    np.seterr(all='ignore')
    c1 = CHOOSE(df['N'], df['O11'])
    c2 = (df['E11'] / df['N']) ** df['O11']
    c3 = (1 - df['E11'] / df['N']) ** (df['N'] - df['O11'])
    am = c1 * c2 * c3
    np.seterr(all='warn')

    return am


##########################
# CONSERVATIVE ESTIMATES #
##########################

def get_poisson_ci_boundary(alpha, O11, R1, O21, R2):
    """
    Get the lower (if O11 / R1 >= O21 / R2) or upper (else) bound of
    the CI of a Poisson distribution

    :param float alpha: sig. level
    :param int O11:
    :param int R1:
    :param int O21:
    :param int R2:
    """

    if O11 == O21 == 0:
        return 0

    if (O11 / R1) >= (O21 / R2):
        lower = beta.ppf(alpha, O11, O21 + 1)
        boundary = max(np.log2((R2 / R1) * lower / (1 - lower)), 0)
    else:
        upper = beta.ppf(1 - alpha, O11 + 1, O21)
        boundary = min(np.log2((R2 / R1) * upper / (1 - upper)), 0)

    return boundary


BOUNDARY = np.vectorize(get_poisson_ci_boundary)


def conservative_log_ratio(df, disc=.5, alpha=.001, boundary='normal',
                           correct='Bonferroni', vocab=None,
                           one_sided=False, **kwargs):
    """
    Calculate conservative log-ratio, i.e. the binary logarithm of the
    lower bound of the confidence interval of relative risk at the
    (Bonferroni-corrected) confidence level.

    :param DataFrame df: pd.DataFrame with columns O11, O12, O21, O22
    :param float disc: discounting (or smoothing) parameter for O11 == 0 and O21 == 0
    :param float alpha: significance level
    :param str boundary: exact CI boundary of [poisson] distribution or [normal] approximation?
    :param str correct: correction type for several tests (None | "Bonferroni" | "Sidak")
    :param int vocab: size of vocabulary (number of comparisons for correcting alpha)
    :param bool one_sided: calculate one- or two-sided confidence interval

    :return: conservative log-ratio
    :rtype: pd.Series

    """

    # correction of alpha for two-sided tests
    if not one_sided:
        alpha /= 2

    # Bonferroni or Sidak correction
    if correct is not None:
        if isinstance(correct, str):
            vocab = (df['O11'] >= 1).sum() if vocab is None else vocab
            if correct == 'Bonferroni':
                alpha /= vocab
            elif correct == "Sidak":
                alpha = 1 - (1 - alpha) ** (1 / vocab)
                # more stable alternative: alpha = 1 - exp(log(1 - alpha) / vocab)
                # doesn't make any difference in practice though, e.g. alpha = .00001, vocab = 10**10
            else:
                raise ValueError('parameter "correct" should either be "Bonferroni" or "Sidak".')
        else:
            raise ValueError('parameter "correct" should either be None or a string.')

    # CONFIDENCE INTERVAL

    # Poisson approximation (Evert 2022)
    if boundary == 'poisson':
        clrr = BOUNDARY(alpha, df['O11'], df['R1'], df['O21'], df['R2'])

    # Normal approximation (Hardie 2014)
    elif boundary == 'normal':
        # - questionable discounting according to Hardie (2014)
        O11_disc = df['O11'].where(df['O11'] != 0, disc)
        O21_disc = df['O21'].where(df['O21'] != 0, disc)
        # - compute natural logarithm of relative risk so we can use estimate for standard error of log(RR)
        lrr = np.log((O11_disc / O21_disc) / (df['R1'] / df['R2']))
        # - asymptotic standard deviation of log(RR) according to Wikipedia
        lrr_sd = np.sqrt(1/O11_disc + 1/O21_disc - 1/df['R1'] - 1/df['R2'])
        # - calculate and apply appropriate boundary
        z_factor = norm.ppf(1 - alpha)
        ci_min = (lrr - lrr_sd * z_factor).clip(lower=0)
        ci_max = (lrr + lrr_sd * z_factor).clip(upper=0)
        clrr = ci_min.where(lrr >= 0, ci_max)
        clrr /= np.log(2)           # adjust to binary logarithm

    return clrr


######################
# INFORMATION THEORY #
######################

def mutual_information(df, disc=.001, **kwargs):
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


def local_mutual_information(df, **kwargs):
    """
    Calculate Local Mutual Information

    :param DataFrame df: pd.DataFrame with columns O11 and E11
    :return: mutual information
    :rtype: pd.Series
    """

    # NB: discounting will not have any effect:
    #     term will be multiplied by original Oij = 0
    O11_disc = df['O11'].where(df['O11'] != 0, 1)
    am = df['O11'] * np.log10(O11_disc / df['E11'])

    return am
