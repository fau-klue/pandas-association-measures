import pytest
from pandas import read_csv, Series
from pandas.testing import assert_series_equal
from numpy import isnan


import association_measures.measures as am
import association_measures.frequencies as fq


@pytest.mark.gold
def test_measures_gold():

    df = read_csv("tests/ucs-gold-100.ds", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)

    # ucs-measures: am.*
    # print([t for t in df.columns if t.startswith('am')])
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

    # calculate module measures
    df_ams = am.calculate_measures(df)
    # print(df_ams.columns)
    # 'z_score',
    # 't_score',
    # 'dice',
    # 'log_likelihood',
    # 'mutual_information',
    # 'hypergeometric_likelihood' NOT IN UCS
    # 'log_ratio' NOT IN UCS

    df = df.join(df_ams)

    assert(round(df['am.Dice'], 10).equals(round(df['dice'], 10)))
    assert(round(df['am.t.score'], 10).equals(round(df['t_score'], 10)))
    assert(round(df['am.z.score'], 10).equals(round(df['z_score'], 10)))
    assert(round(df['am.MI'], 10).equals(round(df['mutual_information'], 10)))
    assert(round(df['am.log.likelihood'], 10).equals(round(df['log_likelihood'], 10)))


# ###########
# # Helpers #
# ###########

@pytest.mark.helpers
def test_phi():

    o = Series([4,3,2,1])
    e = Series([1,2,3,4])

    expected = Series([5.545177, 1.216395, -0.810930, -1.386294])
    actual = am.phi(o, e)

    assert_series_equal(actual, expected)

@pytest.mark.helpers
def test_phi_zero():

    o = Series([0,0,0,0])
    e = Series([0,0,0,0])

    expected = Series([0.0, 0.0, 0.0, 0.0])
    actual = am.phi(o, e)

    assert_series_equal(actual, expected)


######
# MI #
######

@pytest.mark.mi
def test_mutual_information_single(sample_dataframe):

    df = sample_dataframe
    m = df.apply(am.mutual_information, axis=1)
    assert m[0] == 1.0


@pytest.mark.mi
def test_mutual_information(sample_dataframe):

    df = sample_dataframe
    df_ams = am.calculate_measures(df, ['mutual_information'])
    assert df_ams['mutual_information'][0] == 1.0


@pytest.mark.mi
@pytest.mark.nan
def test_mutual_information_nan(invalid_dataframe):
    df = invalid_dataframe

    with pytest.raises(ValueError):
        am.calculate_measures(df, ['mutual_information'])


@pytest.mark.mi
@pytest.mark.zero
def test_mutual_information_with_zeros(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['mutual_information'])
    assert isnan(df_ams['mutual_information'].iloc[0])


########
# DICE #
########

@pytest.mark.dice
def test_dice(sample_dataframe):

    df = sample_dataframe
    df_ams = am.calculate_measures(df, ['dice'])

    assert df_ams['dice'][0] == 1.0


@pytest.mark.dice
@pytest.mark.nan
def test_dice_nan(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['dice'])


@pytest.mark.dice
@pytest.mark.zero
def test_dice_with_zeros(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['dice'])
    assert isnan(df_ams['dice'].iloc[0])


##########
# TSCORE #
##########

@pytest.mark.t_score
def test_t_score_single(sample_dataframe):

    df = sample_dataframe
    m = df.apply(am.t_score, axis=1)
    assert m[0] == 2.846049894151541


@pytest.mark.t_score
def test_t_score(sample_dataframe):

    df = sample_dataframe
    df_ams = am.calculate_measures(df, ['t_score'])
    assert df_ams['t_score'][0] == 2.846049894151541


@pytest.mark.t_score
@pytest.mark.nan
def test_t_score_nan(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['t_score'])


@pytest.mark.t_score
@pytest.mark.zero
def test_t_score_with_zeros(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['t_score'])
    assert isnan(df_ams['t_score'].iloc[0])


##########
# ZSCORE #
##########

@pytest.mark.z_score
def test_z_score(sample_dataframe):

    df = sample_dataframe
    df_ams = am.calculate_measures(df, ['z_score'])
    assert df_ams['z_score'][0] == 9.0


@pytest.mark.z_score
@pytest.mark.nan
def test_z_score_nan(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['z_score'])


@pytest.mark.z_score
@pytest.mark.zero
def test_z_score_with_zeros(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['z_score'])
    assert isnan(df_ams['z_score'].iloc[0])


#############
# LOGLIKELI #
#############

@pytest.mark.log_likelihood
def test_log_likelihood(sample_dataframe):

    df = sample_dataframe
    df_ams = am.calculate_measures(df, ['log_likelihood'])
    assert df_ams['log_likelihood'][0] == 65.01659467828966


@pytest.mark.log_likelihood
@pytest.mark.nan
def test_log_likelihood_nan(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['log_likelihood'])


@pytest.mark.log_likelihood
@pytest.mark.zero
def test_log_likelihood_with_zeros(zero_dataframe):
    df = zero_dataframe
    df_ams = am.calculate_measures(df, ['log_likelihood'])
    assert isnan(df_ams['log_likelihood'].iloc[0])


######
# hypergeometric-likelihood #
######

@pytest.mark.hypergeometric_likelihood
def test_hypergeometric_likelihood(sample_dataframe):
    df = sample_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    # Not available via calculate_measures due to performance issues
    df_ams = am.hypergeometric_likelihood(df)
    assert df_ams[0] == 5.776904234533874e-14


@pytest.mark.hypergeometric_likelihood
@pytest.mark.nan
def test_hypergeometric_likelihood_nan(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.calculate_measures(df, ['hypergeometric_likelihood'])


@pytest.mark.hypergeometric_likelihood
@pytest.mark.zero
def test_hypergeometric_likelihood_with_zeros(zero_dataframe):
    df = zero_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    # Not available via calculate_measures due to performance issues
    ams = am.hypergeometric_likelihood(df)
    assert ams[0] == 1.0
