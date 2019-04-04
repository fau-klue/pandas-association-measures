import pytest
import pandas as pd
import numpy as np

import association.measures as am


@pytest.fixture(scope='function')
def random_dataframe():
    """ Sample DataFrame with random data"""
    df = pd.DataFrame({'f1': np.random.randint(10, size=10),
                       'f2': np.random.randint(10, size=10),
                       'O11': np.random.randint(10, size=10),
                       'N': [10] * 10})
    return df


@pytest.fixture(scope='function')
def sample_dataframe():
    """ Sample DataFrame with fixed data"""
    df = pd.DataFrame({'f1': [10] * 10,
                       'f2': [10] * 10,
                       'O11': [10] * 10,
                       'N': [100] * 10})
    return df


def test_contigency_table(sample_dataframe):
    df = sample_dataframe

    df['O11'], df['O12'], df['O21'], df['O22'] = am.contingency_table(df)
    # TODO: assert

def test_expected_frequencies(sample_dataframe):
    df = sample_dataframe

    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)
    assert df['E11'][0] == 1.0


def test_mutual_information(sample_dataframe):
    df = sample_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.z_score(df)
    df['am'] = am.mutual_information(df)


    assert df['am'][0] == 3.321928094887362


def test_z_score(sample_dataframe):
    df = sample_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.z_score(df)
    assert df['am'][0] == 9.0
