import pytest
import pandas as pd
import numpy as np

import association_measures.frequencies as fq


@pytest.fixture(scope='function')
def invalid_dataframe():
    """ Sample DataFrame with random data"""
    df = pd.DataFrame({'f1': np.random.randint(10, size=10),
                       'f2': np.random.randint(10, size=10),
                       'N': [10] * 10})

    return df


@pytest.fixture(scope='function')
def random_dataframe():
    """ Sample DataFrame with random data"""
    df = pd.DataFrame({'f1': np.random.randint(10, size=10),
                       'f2': np.random.randint(10, size=10),
                       'O11': np.random.randint(10, size=10),
                       'N': [10] * 10})

    df = df.join(fq.expected_frequencies(df))
    return df


@pytest.fixture(scope='function')
def sample_dataframe():
    """ Sample DataFrame with fixed data"""
    df = pd.DataFrame({'f1': [10] * 10,
                       'f2': [10] * 10,
                       'O11': [10] * 10,
                       'N': [100] * 10})

    df = df.join(fq.expected_frequencies(df))
    return df


@pytest.fixture(scope='function')
def zero_dataframe():
    """ Sample DataFrame with zero data"""
    df = pd.DataFrame({'f1': np.zeros(10),
                       'f2': np.zeros(10),
                       'O11': np.zeros(10),
                       'O12': np.zeros(10),
                       'O21': np.zeros(10),
                       'O22': np.zeros(10),
                       'N': np.zeros(10),
                       'E11': np.zeros(10),
                       'E12': np.zeros(10),
                       'E21': np.zeros(10),
                       'E22': np.zeros(10)})

    return df
