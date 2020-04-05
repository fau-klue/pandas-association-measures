import pytest
import numpy as np

import association_measures.measures as am


######
# MI #
######

def test_mutual_information(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.mutual_information(df)
    assert df['am'][0] == 1.0


@pytest.mark.nan
def test_mutual_information_nan(invalid_dataframe):
    df = invalid_dataframe

    df['am'] = am.mutual_information(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_mutual_information_with_zeros(zero_dataframe):
    df = zero_dataframe

    df['am'] = am.mutual_information(df)
    assert np.isnan(df['am'][0])


########
# DICE #
########

@pytest.mark.nan
def test_dice(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.dice(df)
    assert df['am'][0] == 1.0


@pytest.mark.nan
def test_dice_nan(invalid_dataframe):
    df = invalid_dataframe

    df['am'] = am.dice(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_dice_with_zeros(zero_dataframe):
    df = zero_dataframe

    df['am'] = am.dice(df)
    assert np.isnan(df['am'][0])


##########
# TSCORE #
##########

def test_t_score(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.t_score(df)
    assert df['am'][0] == 2.846049894151541


def test_t_score_nan(invalid_dataframe):
    df = invalid_dataframe

    df['am'] = am.t_score(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_t_score_with_zeros(zero_dataframe):
    df = zero_dataframe

    df['am'] = am.t_score(df)
    assert np.isnan(df['am'][0])


##########
# ZSCORE #
##########

def test_z_score(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.z_score(df)
    assert df['am'][0] == 9.0


@pytest.mark.nan
def test_z_score_nan(invalid_dataframe):
    df = invalid_dataframe

    df['am'] = am.z_score(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_z_score_with_zeros(zero_dataframe):
    df = zero_dataframe

    df['am'] = am.z_score(df)
    assert np.isnan(df['am'][0])


#############
# LOGLIKELI #
#############

def test_log_likelihood(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.log_likelihood(df)
    assert df['am'][0] == 65.01659467828966


@pytest.mark.nan
def test_log_likelihood_nan(invalid_dataframe):
    df = invalid_dataframe

    df['am'] = am.log_likelihood(df)
    assert np.isnan(df['am'][0])


@pytest.mark.zero
def test_log_likelihood_with_zeros(zero_dataframe):
    df = zero_dataframe

    df['am'] = am.log_likelihood(df)
    assert df['am'][0] == 0.0


######
# hypergeometric-likelihood #
######

def test_hypergeometric_likelihood(sample_dataframe):
    df = sample_dataframe

    df['am'] = am.hypergeometric_likelihood(df)
    assert df['am'][0] == 8.938031057584301e-09


def test_hypergeometric_likelihood_nan(invalid_dataframe):
    df = invalid_dataframe

    df['am'] = am.hypergeometric_likelihood(df)
    assert np.isnan(df['am'][0])


def test_hypergeometric_likelihood_with_zeros(zero_dataframe):
    df = zero_dataframe

    df['am'] = am.hypergeometric_likelihood(df)
    assert df['am'][0] == 1.0


# Check if any warnings of errors are thrown. Might be an unstable test
@pytest.mark.stability
def test_with_random_data(random_dataframe):
    df = random_dataframe

    df = am.calculate_measures(df)
    assert 't_score' in df.columns
    assert 'z_score' in df.columns
    assert 'dice' in df.columns
    assert 'mutual_information' in df.columns
    assert 'log_likelihood' in df.columns
    assert 'hypergeometric_likelihood' in df.columns
