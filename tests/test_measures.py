import pytest
from numpy import isnan


import association_measures.measures as am
import association_measures.frequencies as fq


######
# MI #
######

@pytest.mark.mi
def test_mutual_information_single(fixed_dataframe):

    df = fq.expected_frequencies(fixed_dataframe, observed=True)
    df_ams = am.mutual_information(df)
    assert df_ams[0] == 1.0


@pytest.mark.mi
def test_mutual_information(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['mutual_information'])
    assert df_ams['mutual_information'][0] == 1.0


@pytest.mark.mi
@pytest.mark.invalid
def test_mutual_information_invalid(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.score(df, ['mutual_information'])


@pytest.mark.mi
@pytest.mark.zero
def test_mutual_information_zero(zero_dataframe):

    df = zero_dataframe
    df_ams = am.score(df, ['mutual_information'])
    assert df_ams['mutual_information'].iloc[0] == 0.061675


############
# LOCAL MI #
############

@pytest.mark.local_mi
def test_local_mi_single(fixed_dataframe):

    df = fq.expected_frequencies(fixed_dataframe, observed=True)
    df_ams = am.local_mutual_information(df)
    assert df_ams[0] == 10.0


@pytest.mark.local_mi
def test_local_mi(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['local_mutual_information'])
    assert df_ams['local_mutual_information'][0] == 10.0


@pytest.mark.local_mi
@pytest.mark.invalid
def test_local_mi_invalid(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.score(df, ['local_mutual_information'])


@pytest.mark.local_mi
@pytest.mark.zero
def test_local_mi_zero(zero_dataframe):

    df = zero_dataframe
    df_ams = am.score(df, ['local_mutual_information'], freq=True)
    assert df_ams['local_mutual_information'].iloc[0] == 848.954896


########
# DICE #
########

@pytest.mark.dice
def test_dice(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['dice'])

    assert df_ams['dice'][0] == 1.0


@pytest.mark.dice
@pytest.mark.invalid
def test_dice_invalid(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.score(df, ['dice'])


@pytest.mark.dice
@pytest.mark.zero
def test_dice_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.score(df, ['dice'])
    assert df_ams['dice'].iloc[0] == 0.168312


##########
# TSCORE #
##########

@pytest.mark.t_score
def test_t_score_single(fixed_dataframe):

    df = fq.expected_frequencies(fixed_dataframe, observed=True)
    m = am.t_score(df)
    assert m[0] == 2.846049894151541


@pytest.mark.t_score
def test_t_score(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['t_score'])
    assert df_ams['t_score'][0] == 2.84605


@pytest.mark.t_score
@pytest.mark.invalid
def test_t_score_invalid(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.score(df, ['t_score'])


@pytest.mark.t_score
@pytest.mark.zero
def test_t_score_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.score(df, ['t_score'], disc=.5)
    assert df_ams['t_score'].iloc[0] == 15.532438


##########
# ZSCORE #
##########

@pytest.mark.z_score
def test_z_score(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['z_score'])
    assert df_ams['z_score'][0] == 9.0


@pytest.mark.z_score
@pytest.mark.invalid
def test_z_score_nan(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.score(df, ['z_score'])


@pytest.mark.z_score
@pytest.mark.zero
def test_z_score_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.score(df, ['z_score'])
    assert df_ams['z_score'].iloc[0] == 16.675431


#################
# LOGLIKELIHOOD #
#################

@pytest.mark.log_likelihood
def test_log_likelihood(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['log_likelihood'])
    assert df_ams['log_likelihood'][0] == 65.016595


@pytest.mark.log_likelihood
@pytest.mark.invalid
def test_log_likelihood_invalid(invalid_dataframe):
    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.score(df, ['log_likelihood'])


@pytest.mark.log_likelihood
@pytest.mark.zero
def test_log_likelihood_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.score(df, ['log_likelihood'], freq=True)
    assert df_ams['log_likelihood'].iloc[0] == 4087.276827


#############
# SIMPLE LL #
#############

@pytest.mark.simple_ll
def test_simple_ll(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['simple_ll'])
    assert df_ams['simple_ll'][0] == 28.051702


@pytest.mark.simple_ll
@pytest.mark.zero
def test_simple_ll_zero(zero_dataframe):
    df = zero_dataframe
    df_ams = am.score(df, ['simple_ll'], freq=True)
    assert df_ams['simple_ll'].iloc[0] == 264.915789


#############################
# hypergeometric likelihood #
#############################
# Not available via score due to numerical instability

@pytest.mark.choose
@pytest.mark.hypergeometric_likelihood
def test_hypergeometric_likelihood(fixed_dataframe):
    df = fq.expected_frequencies(fixed_dataframe, observed=True)
    df_ams = am.hypergeometric_likelihood(df)
    assert round(df_ams[0], 20) == 5.776904e-14


@pytest.mark.choose
@pytest.mark.hypergeometric_likelihood
def test_hypergeometric_likelihood_brown_overflow(brown_dataframe):
    df = fq.expected_frequencies(brown_dataframe, observed=True).head(10)
    df['hypergeometric_likelihood'] = am.hypergeometric_likelihood(df)
    assert df['hypergeometric_likelihood'].isnull().any()


@pytest.mark.choose
@pytest.mark.hypergeometric_likelihood
@pytest.mark.zero
def test_hypergeometric_likelihood_zero(zero_dataframe):
    df = fq.expected_frequencies(zero_dataframe, observed=True)
    ams = am.hypergeometric_likelihood(df)
    assert isnan(ams[0])


#######################
# binomial likelihood #
#######################
# Not available via score due to numerical instability

@pytest.mark.choose
@pytest.mark.binomial_likelihood
def test_binomial_likelihood(fixed_dataframe):
    df = fq.expected_frequencies(fixed_dataframe, observed=True)
    df_ams = am.binomial_likelihood(df)
    assert round(df_ams[0], 14) == 7.006036e-08


@pytest.mark.choose
@pytest.mark.binomial_likelihood
def test_binomial_likelihood_brown(brown_dataframe):
    df = brown_dataframe
    df = df.join(fq.observed_frequencies(df), rsuffix='_')
    df = df.join(fq.expected_frequencies(df), rsuffix='_')
    df = df.head(100)
    df['binomial_likelihood'] = am.binomial_likelihood(df)
    assert round(df['binomial_likelihood'][0], 6) == 0.008101


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
    df = fq.expected_frequencies(zero_dataframe, observed=True)
    ams = am.binomial_likelihood(df)
    assert isnan(ams.iloc[0])


#############
# Log Ratio #
#############

@pytest.mark.log_ratio
def test_log_ratio(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['log_ratio'], disc=.5, discounting='Hardie2014')
    assert df_ams['log_ratio'].iloc[0] == 7.491853


@pytest.mark.log_ratio
@pytest.mark.invalid
def test_log_ratio_invalid(invalid_dataframe):

    df = invalid_dataframe
    with pytest.raises(ValueError):
        am.score(df, ['log_ratio'])


@pytest.mark.log_ratio
@pytest.mark.zero
def test_log_ratio_zero(zero_dataframe):

    df = zero_dataframe
    df_ams = am.score(df, ['log_ratio'], disc=.5, discounting='Hardie2014')
    assert df_ams['log_ratio'].iloc[0] == 12.03645


##########################
# Conservative Log Ratio #
##########################

@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['log_ratio', 'conservative_log_ratio'], boundary='normal', disc=.5, alpha=.01)
    assert (abs(df_ams['log_ratio']) >= abs(df_ams['conservative_log_ratio'])).all()
    assert df_ams['conservative_log_ratio'].iloc[0] == 0.796936


@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio_zero(zero_dataframe):

    df = zero_dataframe
    df_ams = am.score(df, ['log_ratio', 'conservative_log_ratio'])
    assert (abs(df_ams['log_ratio']) >= abs(df_ams['conservative_log_ratio'])).all()


@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio_zero_poisson(zero_dataframe):

    df = zero_dataframe
    df_ams = am.score(df, ['log_ratio', 'conservative_log_ratio'], boundary='poisson')
    assert (abs(df_ams['log_ratio']) >= abs(df_ams['conservative_log_ratio'])).all()


@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio_zero_poisson_sig(zero_dataframe_sig):

    df = zero_dataframe_sig
    df_ams = am.score(df, ['log_ratio', 'conservative_log_ratio'], boundary='poisson')
    assert (abs(df_ams['log_ratio']) >= abs(df_ams['conservative_log_ratio'])).all()


@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio_one_sided(fixed_dataframe):

    df = fq.expected_frequencies(fixed_dataframe, observed=True)
    df_ams = am.score(df, ['conservative_log_ratio'], boundary='normal')
    df_am = am.conservative_log_ratio(df, one_sided=True, boundary='normal')
    df_am.name = 'clr_one_sided'
    df_ams = df_ams.join(df_am)
    assert (abs(df_ams['conservative_log_ratio']) <= abs(df_ams['clr_one_sided'])).all()


@pytest.mark.conservative_log_ratio
def test_conservative_log_ratio_boundaries(brown_dataframe):

    df = brown_dataframe
    df_ams = am.score(df, ['conservative_log_ratio'])
    df_am = am.score(df, ['conservative_log_ratio'], boundary="normal")['conservative_log_ratio']
    df_am.name = 'clr_normal'
    df_ams = df_ams.join(df_am)
    assert (df_ams['clr_normal'] == 0).sum() < (df_ams['conservative_log_ratio'] == 0).sum()


###################
# MIN_SENSITIVITY #
###################

@pytest.mark.min_sensitivity
def test_min_sensitivity(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['min_sensitivity'])
    assert df_ams['min_sensitivity'][0] == 1


###########
# LIDDELL #
###########

@pytest.mark.liddell
def test_liddell(fixed_dataframe):

    df = fixed_dataframe
    df_ams = am.score(df, ['liddell'])
    assert df_ams['liddell'].iloc[0] == 1


@pytest.mark.liddell
def test_liddell_zero(zero_dataframe):

    df = fq.expected_frequencies(zero_dataframe, observed=True)
    df_ams = am.score(df, ['liddell'])
    assert df_ams['liddell'].iloc[0] == 0.143858


########
# GOLD #
########

@pytest.mark.gold
def test_measures_ucs_gold(ucs_dataframe):

    df = ucs_dataframe
    df = df.join(am.score(df, freq=False))

    for ucs, assoc in [('am.Dice', 'dice'),
                       ('am.MS', 'min_sensitivity'),
                       ('am.t.score', 't_score'),
                       ('am.z.score', 'z_score'),
                       ('am.MI', 'mutual_information'),
                       ('am.log.likelihood', 'log_likelihood'),
                       ('am.local.MI', 'local_mutual_information'),
                       ('am.simple.ll', 'simple_ll')]:

        assert round(df[ucs], 6).equals(df[assoc])


@pytest.mark.gold
def test_measures_log_ratio_gold(log_ratio_dataframe):

    df = log_ratio_dataframe
    df = df.join(am.score(df, ['log_ratio', 'conservative_log_ratio'], boundary='normal',
                          discounting='Hardie2014', disc=.5, alpha=.01, freq=False))

    for r, assoc in [('lr', 'log_ratio'),
                     ('clr', 'conservative_log_ratio')]:

        assert round(df[r], 6).equals(df[assoc])


@pytest.mark.gold
def test_measures_lrc_gold(log_ratio_dataframe):

    # original implementation with normal approximation
    df = log_ratio_dataframe
    df = df.join(am.score(df, ['conservative_log_ratio'], boundary='normal', alpha=.05, freq=False))
    assert df['conservative_log_ratio'].equals(round(df['lrc.normal'], 6))

    # implementation with poisson approximation
    df = log_ratio_dataframe
    df = df.join(am.score(df, ['conservative_log_ratio'],
                          alpha=.05, boundary='poisson', freq=False))
    assert df['conservative_log_ratio'].equals(round(df['lrc'], 6))


#################
# SCORE WRAPPER #
#################
@pytest.mark.score
def test_score_notation(ucs_dataframe):

    # frequency signature notation in dataframe:
    df1 = am.score(ucs_dataframe)

    # frequency signature notation with int parameters:
    f1 = int(ucs_dataframe['f1'].iloc[0])
    N = int(ucs_dataframe['N'].iloc[0])
    df2 = am.score(ucs_dataframe[['f', 'f2']], f1=f1, N=N)

    # corpus frequency notation in dataframe:
    tmp = ucs_dataframe[['f', 'f1']].rename({'f': 'f1', 'f1': 'N1'}, axis=1)
    tmp['N2'] = ucs_dataframe['N'] - ucs_dataframe['f1']
    tmp['f2'] = ucs_dataframe['f2'] - ucs_dataframe['f']
    df3 = am.score(tmp)

    # corpus frequency notation with int parameters:
    N1 = int(tmp['N1'].iloc[0])
    N2 = int(tmp['N2'].iloc[0])
    df4 = am.score(tmp[['f1', 'f2']], N1=N1, N2=N2)

    assert df1.equals(df2)
    assert df2.equals(df3)
    assert df3.equals(df4)


@pytest.mark.score
def test_score_invalid(ucs_dataframe):

    with pytest.raises(ValueError):
        am.score(ucs_dataframe, f1=1, N1=1)

    with pytest.raises(ValueError):
        am.score(ucs_dataframe, N2=1)

    with pytest.raises(ValueError):
        am.score(ucs_dataframe, f1=1, N2=1)


def test_calculate_measures(zero_dataframe):
    df = zero_dataframe
    with pytest.deprecated_call():
        df_ams = am.calculate_measures(df, ['dice'])
    df_ams['dice'].iloc[0] == 0.16831229174945742
