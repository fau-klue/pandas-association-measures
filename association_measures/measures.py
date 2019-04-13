"""
Association measures are mathematical formulae that interpret cooccurrence frequency data.

http://www.collocations.de/AM/index.html
"""


import pandas as pd
import numpy as np
from .binomial import choose as binomial


choose = np.vectorize(binomial) # pylint: disable=invalid-name


def z_score(df):
    """
    Calculate z-score

    :param pandas.DataFrame df: Pandas Dataframe containing O11 and E11
    :return: pandas.Series containing the Z-Score for each token
    :rtype: pandas.Series
    """

    if 'E11' not in df.columns:
        return np.nan

    res = (df['O11'] - df['E11']) / np.sqrt(df['E11'])

    return pd.Series(data=res)


def t_score(df):
    """
    Calculate t-score

    :param pandas.DataFrame df: Pandas Dataframe containing O11 and E11
    :return: pandas.Series containing the T-Score for each token
    :rtype: pandas.Series
    """

    if 'E11' not in df.columns:
        return np.nan

    res = (df['O11'] - df['E11']) / np.sqrt(df['O11'])

    return pd.Series(data=res)


def mutual_information(df):
    """
    Calculate Mutual Information

    :param pandas.DataFrame df: Pandas Dataframe containing O11 and E11
    :return: pandas.Series containing the Mutual Information score for
    each token
    :rtype: pandas.Series
    """

    if 'E11' not in df.columns:
        return np.nan

    diff = df['E11'].replace(0, np.nan) / df['O11'].replace(0, np.nan)
    res = np.log(diff.replace(0.0, np.nan))

    return pd.Series(data=res)


def dice(df):
    """
    Calculate Dice coefficient

    :param pandas.DataFrame df: Pandas Dataframe containing O11, f1 and f2
    :return: pandas.Series containing the Dice coefficient for each token
    :rtype: pandas.Series
    """

    if 'O11' not in df.columns:
        return np.nan

    res = (2 * df['O11']) / (df['f1'] + df['f2'])

    return pd.Series(data=res)


def log_likelihood(df):
    """
    Calculate log-likelihood

    :param pandas.DataFrame df: Pandas Dataframe containing O11, O12,
    O21, O22, E11, E12, E21 and E22
    :return: pandas.Series containing the log-likelihood score for each token
    :rtype: pandas.Series
    """

    if 'E11' not in df.columns:
        return np.nan

    with np.errstate(divide='ignore', invalid='ignore'):
        ii = df['O11'] * np.log(df['O11'] / df['E11'].replace(0, np.nan))
        ij = df['O12'] * np.log(df['O12'] / df['E12'].replace(0, np.nan))
        ji = df['O21'] * np.log(df['O21'] / df['E21'].replace(0, np.nan))
        jj = df['O22'] * np.log(df['O22'] / df['E22'].replace(0, np.nan))

    res = 2 * pd.concat([ii, ij, ji, jj], axis=1).sum(1)

    return pd.Series(data=res)


def hypergeometric_likelihood(df):
    """
    Calculate hypergeometric-likelihood

    :param pandas.DataFrame df: Pandas Dataframe containing O11, O12,
    O21, O22, E11, E12, E21 and E22
    :return: pandas.Series containing the hypergeometric-likelihood score for each token
    :rtype: pandas.Series
    """

    if 'O11' not in df.columns:
        return np.nan

    # TODO: Is this correct?
    res = (
        choose(df['f2'], df['O11']) *
        choose(df['O12'] + df['O22'], df['f1'] - df['O11'])
    ) / choose(df['N'], df['f1'])

    return pd.Series(data=res)


def calculate_measures(df, measures=None):
    """
    Calculate a list of association measures. Defaults to all available measures.

    :param pandas.DataFrame df: Pandas Dataframe containing O11, O12,
    O21, O22, E11, E12, E21 and E22
    :return: pandas.DataFrame containing all available association measures
    :rtype: pandas.DataFrame
    """

    if not measures:
        measures = [z_score,
                    t_score,
                    dice,
                    log_likelihood,
                    mutual_information,
                    hypergeometric_likelihood]

    for measure in measures:
        df[measure.__name__] = measure(df)

    return df
