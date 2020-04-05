from pandas import read_csv


import association_measures.frequencies as fq
import association_measures.measures as am


def test_frequencies():

    df = read_csv("tests/ucs-gold.ds.gz", comment='#', index_col=0,
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
    df['o11'], df['o12'], df['o21'], df['o22'] = fq.observed_frequencies(df)
    assert(df['o11'].equals(df['O11']))
    assert(df['o12'].equals(df['O12']))
    assert(df['o21'].equals(df['O21']))
    assert(df['o22'].equals(df['O22']))

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
    df['e11'], df['e12'], df['e21'], df['e22'] = fq.expected_frequencies(df)
    assert(df['e11'].equals(df['E11']))
    assert(df['e12'].equals(df['E12']))
    assert(df['e21'].equals(df['E21']))
    assert(df['e22'].equals(df['E22']))


def test_measures():

    df = read_csv("tests/ucs-gold.ds.gz", comment='#', index_col=0,
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
    df = am.calculate_measures(df)
    # print(df.columns)
    # 'z_score',
    # 't_score',
    # 'dice',
    # 'log_likelihood',
    # 'mutual_information',
    # 'hypergeometric_likelihood' NOT IN UCS
    # 'log_ratio' NOT IN UCS

    assert(round(df['am.Dice'], 10).equals(round(df['dice'], 10)))
    assert(round(df['am.t.score'], 10).equals(round(df['t_score'], 10)))
    assert(round(df['am.z.score'], 10).equals(round(df['z_score'], 10)))
    assert(round(df['am.MI'], 10).equals(round(df['mutual_information'], 10)))
    assert(round(df['am.log.likelihood'], 10).equals(round(df['log_likelihood'], 10)))
