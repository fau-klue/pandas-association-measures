import association_measures.frequencies as fq
from pandas import read_csv


def test_observed_frequencies(sample_dataframe):

    df = fq.observed_frequencies(sample_dataframe)

    assert df['O11'][0] == 10
    assert df['O12'][0] == 0
    assert df['O21'][0] == 0
    assert df['O22'][0] == 90


def test_expected_frequencies(sample_dataframe):

    df = fq.expected_frequencies(sample_dataframe)

    assert df['E11'][0] == 1.0


def test_gold():

    df = read_csv("tests/ucs-gold-100.ds", comment='#', index_col=0,
                  sep="\t", quoting=3, keep_default_na=False)

    # ucs data has the following relevant columns
    # f = O11
    # f1 = R1
    # f2 = C1
    # N

    # get observed frequencies
    df['O11'] = df['f']
    df['O21'] = df['f2'] - df['O11']
    df['O12'] = df['f1'] - df['O11']
    df['O22'] = df['N'] - df['f1'] - df['O21']

    # check observed frequencies
    obs = fq.observed_frequencies(df)
    assert(obs['O11'].equals(df['O11']))
    assert(obs['O12'].equals(df['O12']))
    assert(obs['O21'].equals(df['O21']))
    assert(obs['O22'].equals(df['O22']))

    # check marginals
    R1 = df['O11'] + df['O12']
    R2 = df['O21'] + df['O22']
    C1 = df['O11'] + df['O21']
    C2 = df['O12'] + df['O22']
    assert((R1 + R2).equals(df['N']))
    assert((C1 + C2).equals(df['N']))

    # get expected frequencies
    df['E11'] = R1 * C1 / df['N']
    df['E12'] = R1 * C2 / df['N']
    df['E21'] = R2 * C1 / df['N']
    df['E22'] = R2 * C2 / df['N']

    # check expected frequencies
    exp = fq.expected_frequencies(df)
    assert(exp['E11'].equals(df['E11']))
    assert(exp['E12'].equals(df['E12']))
    assert(exp['E21'].equals(df['E21']))
    assert(exp['E22'].equals(df['E22']))
