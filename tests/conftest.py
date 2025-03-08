import pytest
import pandas as pd
import numpy as np


@pytest.fixture(scope='function')
def fixed_dataframe():
    """ Sample DataFrame with fixed data in freq. signature notation """

    df = pd.DataFrame({'f': list(reversed(range(1, 11))),
                       'f1': [10] * 10,
                       'f2': list(range(10, 30, 2)),
                       'N': [100] * 10})

    return df


@pytest.fixture(scope='function')
def invalid_dataframe():
    """ Sample DataFrame with missing data in freq. signature notation """

    df = pd.DataFrame({'f1': np.random.randint(10, size=10),
                       'f2': np.random.randint(10, size=10),
                       'N': [10] * 10})

    return df


@pytest.fixture(scope='function')
def random_dataframe():
    """ Sample DataFrame with random data in freq. signature notation

    invalid if f > f1
    """

    df = pd.DataFrame({'f': np.random.randint(10, size=10),
                       'f1': np.random.randint(10, size=10),
                       'f2': np.random.randint(10, size=10),
                       'N': [10] * 10})

    return df


@pytest.fixture(scope='function')
def zero_dataframe():
    """ Sample DataFrame with lots of zeros in contingency notation """

    df = pd.read_csv("tests/data/df-zeros.tsv", index_col=0,
                     sep="\t", quoting=3, keep_default_na=False)

    return df


@pytest.fixture(scope='function')
def zero_dataframe_sig():
    """ Sample DataFrame with lots of zeros in freq. signature notation """

    df = pd.read_csv("tests/data/df-zeros-sig.tsv", index_col=0,
                     sep="\t", quoting=3, keep_default_na=False)

    return df


@pytest.fixture(scope='function')
def ucs_dataframe():
    """ Sample DataFrame with real data and calculations from UCS.
    Freq. signature notation.

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
    df = pd.read_csv("tests/data/ucs-gold-100.ds", comment='#', index_col=0,
                     sep="\t", quoting=3, keep_default_na=False)

    return df


@pytest.fixture(scope='function')
def log_ratio_dataframe():
    """Sample DataFrame with real data and calculations from
    R-implementation that has been cross-checked via
    CQPweb. Freq. signature notation.

    available measures:
    # 'lr'
    # 'clr'
    # 'lrc'
    # 'lrc.positive'
    # 'lrc.normal'

    """
    df = pd.read_csv("tests/data/log-ratio-gold.tsv", index_col=0, sep="\t")

    return df


@pytest.fixture(scope='function')
def brown_dataframe():
    """Sample DataFrame with real data counts from Brown
    Corpus. Freq. signature notation.

    """
    df = pd.read_csv("tests/data/brown.csv", index_col=0)

    return df


@pytest.fixture(scope='function')
def rbo_dataframe():
    """RBO calculations on log-ratio-gold calculated using gespeR.

    """
    df = pd.read_csv("tests/data/rbo.tsv", sep="\t")

    return df
