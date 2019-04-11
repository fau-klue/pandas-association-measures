import pytest

import association_measures.frequencies as fq


def test_observed_frequencies(sample_dataframe):
    df = sample_dataframe

    df['O11'], df['O12'], df['O21'], df['O22'] = fq.observed_frequencies(df)
    assert df['O11'][0] == 10
    assert df['O12'][0] == 0
    assert df['O21'][0] == 0
    assert df['O22'][0] == 90


def test_expected_frequencies(sample_dataframe):
    df = sample_dataframe
    df['E11'], df['E12'], df['E21'], df['E22'] = fq.expected_frequencies(df)

    assert df['E11'][0] == 1.0
