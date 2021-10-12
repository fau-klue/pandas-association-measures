import pytest
from pandas import Series
from pandas.testing import assert_series_equal
from numpy import isnan


import association_measures.measures as am
import association_measures.frequencies as fq


###########
# Helpers #
###########

@pytest.mark.helpers
def test_phi():

    o = Series([4, 3, 2, 1])
    e = Series([1, 2, 3, 4])

    expected = Series([5.545177, 1.216395, -0.810930, -1.386294])
    actual = am.phi(o, e)

    assert_series_equal(actual, expected)


@pytest.mark.helpers
def test_phi_zero():

    o = Series([0, 0, 0, 0])
    e = Series([0, 0, 0, 0])

    expected = Series([0.0, 0.0, 0.0, 0.0])
    actual = am.phi(o, e)

    assert_series_equal(actual, expected)


######
# MI #
######

@pytest.mark.mi
def test_mutual_information_single(fixed_dataframe):

    df = fixed_dataframe
    m = df.apply(am.mutual_information, axis=1)
    assert m[0] == 1.0


@pytest.mark.mi
def test_mutual_information(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['mutual_information'])
    assert df_ams['mutual_information'][0] == 1.0


@pytest.mark.mi
@pytest.mark.invalid
def test_mutual_information_invalid(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['mutual_information'])


@pytest.mark.mi
@pytest.mark.zero
def test_mutual_information_zero(zero_dataframe):

    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['mutual_information'])
    assert isnan(df_ams['mutual_information'].iloc[0])


########
# DICE #
########

@pytest.mark.dice
def test_dice(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['dice'])

    assert df_ams['dice'][0] == 1.0


@pytest.mark.dice
@pytest.mark.invalid
def test_dice_invalid(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['dice'])


@pytest.mark.dice
@pytest.mark.zero
def test_dice_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['dice'])
    assert isnan(df_ams['dice'].iloc[0])


##########
# TSCORE #
##########

@pytest.mark.t_score
def test_t_score_single(fixed_dataframe):

    df = fixed_dataframe
    m = df.apply(am.t_score, axis=1)
    assert m[0] == 2.846049894151541


@pytest.mark.t_score
def test_t_score(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['t_score'])
    assert df_ams['t_score'][0] == 2.846049894151541


@pytest.mark.t_score
@pytest.mark.invalid
def test_t_score_invalid(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['t_score'])


@pytest.mark.t_score
@pytest.mark.zero
def test_t_score_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['t_score'])
    assert isnan(df_ams['t_score'].iloc[0])


##########
# ZSCORE #
##########

@pytest.mark.z_score
def test_z_score(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['z_score'])
    assert df_ams['z_score'][0] == 9.0


@pytest.mark.z_score
@pytest.mark.invalid
def test_z_score_nan(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['z_score'])


@pytest.mark.z_score
@pytest.mark.zero
def test_z_score_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['z_score'])
    assert isnan(df_ams['z_score'].iloc[0])


#################
# LOGLIKELIHOOD #
#################

@pytest.mark.log_likelihood
def test_log_likelihood(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['log_likelihood'])
    assert df_ams['log_likelihood'][0] == 65.01659467828966


@pytest.mark.log_likelihood
@pytest.mark.invalid
def test_log_likelihood_invalid(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['log_likelihood'])


@pytest.mark.log_likelihood
@pytest.mark.zero
def test_log_likelihood_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['log_likelihood'])
    assert df_ams['log_likelihood'].iloc[0] == 0.0


#############################
# hypergeometric likelihood #
#############################
# Not available via calculate_measures due to numerical instability

@pytest.mark.choose
@pytest.mark.hypergeometric_likelihood
def test_hypergeometric_likelihood(fixed_dataframe):
    df = fixed_dataframe
    df_ams = am.hypergeometric_likelihood(df)
    assert df_ams[0] == 5.776904234533874e-14


@pytest.mark.choose
@pytest.mark.hypergeometric_likelihood
def test_hypergeometric_likelihood_brown_overflow(brown_dataframe):
    df = brown_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    df = df.head(10)
    df['hypergeometric_likelihood'] = am.hypergeometric_likelihood(df)
    assert df['hypergeometric_likelihood'].isnull().any()


@pytest.mark.choose
@pytest.mark.hypergeometric_likelihood
@pytest.mark.zero
def test_hypergeometric_likelihood_zero(zero_dataframe):
    df = zero_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    ams = am.hypergeometric_likelihood(df)
    assert ams[0] == 1.0


#############################
# binomial likelihood #
#############################
# Not available via calculate_measures due to numerical instability

@pytest.mark.choose
@pytest.mark.binomial_likelihood
def test_binomial_likelihood(fixed_dataframe):
    df = fixed_dataframe
    df_ams = am.binomial_likelihood(df)
    assert df_ams[0] == 7.006035693977206e-08


@pytest.mark.choose
@pytest.mark.binomial_likelihood
def test_binomial_likelihood_brown(brown_dataframe):
    df = brown_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    df = df.join(fq.expected_frequencies(df), rsuffix='_')
    df = df.head(100)
    df['binomial_likelihood'] = am.binomial_likelihood(df)
    assert df['binomial_likelihood'][0] == 0.02277706874213509


@pytest.mark.choose
@pytest.mark.binomial_likelihood
def test_binomial_likelihood_brown_overflow(brown_dataframe):
    df = brown_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    df = df.join(fq.expected_frequencies(df), rsuffix='_')
    df = df.head(1000)
    df['binomial_likelihood'] = am.binomial_likelihood(df)
    assert df['binomial_likelihood'].isnull().any()


@pytest.mark.choose
@pytest.mark.binomial_likelihood
@pytest.mark.zero
def test_binomial_likelihood_zero(zero_dataframe):
    df = zero_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    ams = am.binomial_likelihood(df)
    assert ams[0] == 1.0


#############
# Log Ratio #
#############

@pytest.mark.log_ratio
def test_log_ratio(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['log_ratio'])
    assert df_ams['log_ratio'][0] == 7.491853096329675


@pytest.mark.log_ratio
@pytest.mark.invalid
def test_log_ratio_invalid(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['log_ratio'])


@pytest.mark.log_ratio
@pytest.mark.zero
def test_log_ratio_zero(zero_dataframe):

    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['log_ratio'])
    assert isnan(df_ams['log_ratio'].iloc[0])


##########################
# Conservative Log Ratio #
##########################

@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['log_ratio', 'conservative_log_ratio'])
    assert((abs(df_ams['log_ratio']) >= abs(df_ams['conservative_log_ratio'])).all())
    assert(df_ams['conservative_log_ratio'].iloc[0] == 0.7969356993077386)


@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio_one_sided(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.calculate_measures(df, ['conservative_log_ratio'])
    df_am = am.conservative_log_ratio(df, one_sided=True)
    df_am.name = 'clr_one_sided'
    df_ams = df_ams.join(df_am)
    assert((abs(df_ams['conservative_log_ratio']) <= abs(df_ams['clr_one_sided'])).all())


########
# GOLD #
########

@pytest.mark.gold
def test_measures_ucs(ucs_dataframe):

    df = ucs_dataframe
    df = df.join(am.calculate_measures(df))

    for ucs, assoc in [('am.Dice', 'dice'),
                       ('am.t.score', 't_score'),
                       ('am.z.score', 'z_score'),
                       ('am.MI', 'mutual_information'),
                       ('am.log.likelihood', 'log_likelihood')]:

        assert(round(df[ucs], 10).equals(round(df[assoc], 10)))


@pytest.mark.gold
def test_measures_log_ratio_gold(log_ratio_dataframe):

    df = log_ratio_dataframe
    df = df.join(am.calculate_measures(df, ['log_ratio', 'conservative_log_ratio']))

    for r, assoc in [('lr', 'log_ratio'),
                     ('clr', 'conservative_log_ratio')]:

        assert(round(df[r], 3).equals(round(df[assoc], 3)))
