import pytest
import pandas as pd
import numpy as np

import association_measures.measures as am


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


@pytest.fixture(scope='function')
def zero_dataframe():
    """ Sample DataFrame with zero data"""
    df = pd.DataFrame({'f1': np.zeros(10),
                       'f2': np.zeros(10),
                       'O11': np.zeros(10),
                       'N': np.zeros(10)})
    return df


def test_contigency_table(sample_dataframe):
    df = sample_dataframe

    df['O11'], df['O12'], df['O21'], df['O22'] = am.contingency_table(df)
    assert df['O11'][0] == 10
    assert df['O12'][0] == 0
    assert df['O21'][0] == 0
    assert df['O22'][0] == 90


def test_expected_frequencies(sample_dataframe):
    df = sample_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    assert df['E11'][0] == 1.0


def test_mutual_information(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.mutual_information(df)
    assert np.isnan(df['am'][0])

    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.mutual_information(df)
    assert df['am'][0] == -2.3025850929940455


def test_z_score(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.z_score(df)
    assert np.isnan(df['am'][0])

    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.z_score(df)
    assert df['am'][0] == 9.0


def test_t_score(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.t_score(df)
    assert np.isnan(df['am'][0])

    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.t_score(df)
    assert df['am'][0] == 2.846049894151541


def test_dice(sample_dataframe):
    df = sample_dataframe

    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.dice(df)
    assert df['am'][0] == 1.0


def test_log_likelihood(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.log_likelihood(df)
    assert np.isnan(df['am'][0])

    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.log_likelihood(df)
    assert df['am'][0] == 65.01659467828966


@pytest.mark.zero
def test_log_likelihood_with_zeros(zero_dataframe):
    df = zero_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.log_likelihood(df)
    assert df['am'][0] == 0.0


@pytest.mark.zero
def test_dice_with_zeros(zero_dataframe):
    df = zero_dataframe
    df['am'] = am.dice(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_z_score_with_zeros(zero_dataframe):
    df = zero_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.z_score(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_t_score_with_zeros(zero_dataframe):
    df = zero_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.t_score(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_mutual_information_with_zeros(zero_dataframe):
    df = zero_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    df['am'] = am.mutual_information(df)
    assert np.isnan(df['am'][0])


@pytest.mark.stability
def test_with_random_data(random_dataframe):
    df = random_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)

    # Check if any warnings of errors are thrown. Might be an unstable test
    df['ts'] = am.t_score(df)
    df['zs'] = am.z_score(df)
    df['di'] = am.dice(df)
    df['mi'] = am.mutual_information(df)
    df['ll'] = am.log_likelihood(df)
