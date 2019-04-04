import pytest
import pandas as pd
import numpy as np

import association.measures as am


@pytest.fixture(scope='function')
def random_dataframe():
    """ Sample DataFrame with random data"""
    df = pd.DataFrame({'f1': np.random.randint(100, size=10),
                       'f2': np.random.randint(100, size=10),
                       'O11': np.random.randint(100, size=10),
                       'N': [100] * 10})
    return df


@pytest.fixture(scope='function')
def sample_dataframe():
    """ Sample DataFrame with fixed data"""
    df = pd.DataFrame({'f1': [10] * 10,
                       'f2': [10] * 10,
                       'O11': [10] * 10,
                       'N': [100] * 10})
    return df


def test_expected_frequencies(sample_dataframe):
    df = sample_dataframe

    df['E11'] = df.apply(am.expected_frequencies, axis=1)
    assert df['E11'][0] == 1.0


def test_contigency_table(sample_dataframe):
    df = sample_dataframe

    df[['O12', 'O21', 'O22']] = df.apply(am.contingency_table, axis=1)
    # TODO: assert


def test_mutual_information(sample_dataframe):
    df = sample_dataframe
    df['E11'] = df.apply(am.expected_frequencies, axis=1)

    df['mi'] = df.apply(am.mutual_information, axis=1)
    assert df['mi'][0] == 3.321928094887362


def test_z_score(sample_dataframe):
    df = sample_dataframe
    df['E11'] = df.apply(am.expected_frequencies, axis=1)

    df['z_score'] = df.apply(am.z_score, axis=1)
    assert df['z_score'][0] == 9.0
