import pytest
import pandas as pd
import numpy as np

import association_measures.frequencies as fq


@pytest.fixture(scope='function')
def fixed_dataframe():
    """ Sample DataFrame with fixed data"""
    df = pd.DataFrame({'f': list(reversed(range(1, 11))),
                       'f1': [10] * 10,
                       'f2': list(range(10, 30, 2)),
                       'N': [100] * 10})
    df = df.join(fq.observed_frequencies(df))
    df = df.join(fq.expected_frequencies(df))
    return df


@pytest.fixture(scope='function')
def invalid_dataframe():
    """ Sample DataFrame with missing data """
    df = pd.DataFrame({'f1': np.random.randint(10, size=10),
                       'f2': np.random.randint(10, size=10),
                       'N': [10] * 10})

    return df


@pytest.fixture(scope='function')
def random_dataframe():
    """ Sample DataFrame with random data

    invalid if f > f1
    """
    df = pd.DataFrame({'f': np.random.randint(10, size=10),
                       'f1': np.random.randint(10, size=10),
                       'f2': np.random.randint(10, size=10),
                       'N': [10] * 10})

    df = df.join(fq.observed_frequencies(df))
    df = df.join(fq.expected_frequencies(df))
    return df


@pytest.fixture(scope='function')
def zero_dataframe():
    """ Sample DataFrame with lots of zeros """

    df = pd.read_csv("tests/df-zeros.tsv", index_col=0,
                     sep="\t", quoting=3, keep_default_na=False)

    return df


@pytest.fixture(scope='function')
def ucs_dataframe():
    """ Sample DataFrame with real data and calculations from UCS

    available measures:
    # 'am.Dice',
    # 'am.Fisher.pv',
    # 'am.Jaccard',
    # 'am.MI',
    # 'am.MI2',
    # 'am.MI3',
    # 'am.MS',
    # 'am.Poisson.Stirling',
    # 'am.Poisson.pv',
    # 'am.average.MI',
    # 'am.chi.squared',
    # 'am.chi.squared.corr',
    # 'am.frequency',
    # 'am.gmean',
    # 'am.local.MI',
    # 'am.log.likelihood',
    # 'am.odds.ratio',
    # 'am.odds.ratio.disc',
    # 'am.random',
    # 'am.relative.risk',
    # 'am.simple.ll',
    # 'am.t.score',
    # 'am.z.score',
    # 'am.z.score.corr'

    """
    df = pd.read_csv("tests/ucs-gold-100.ds", comment='#', index_col=0,
                     sep="\t", quoting=3, keep_default_na=False)

    return df


@pytest.fixture(scope='function')
def log_ratio_dataframe():
    """ Sample DataFrame with real data and calculations
    from R-implementation that has been cross-checked via CQPweb

    available measures:
    # 'lr'
    # 'clr'

    """
    df = pd.read_csv("tests/log-ratio-gold.tsv", index_col=0, sep="\t")

    return df


@pytest.fixture(scope='function')
def brown_dataframe():
    """ Sample DataFrame with real data counts from Brown Corpus.

    """
    df = pd.read_csv("tests/brown.csv", index_col=0)

    return df
