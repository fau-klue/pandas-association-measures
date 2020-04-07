[![Build Status](https://travis-ci.org/fau-klue/pandas-association-measures.svg?branch=master)](https://travis-ci.org/fau-klue/pandas-association-measures)
[![Coverage Status](https://coveralls.io/repos/github/fau-klue/pandas-association-measures/badge.svg?branch=master)](https://coveralls.io/github/fau-klue/pandas-association-measures?branch=master)

# Corpus Association Measures for Python pandas

> Association measures are mathematical formulae that interpret cooccurrence frequency data. For each pair of words extracted from a corpus, they compute an association score, a single real value that indicates the amount of (statistical) association between the two words.

http://www.collocations.de/AM/index.html

# Installation

Using pip:

    pip install association-measures

From Source:

    # Compile Cython code (requires Cython)
    python setup.py build_ext --inplace

    # Cython already compiled
    python setup.py install

# Usage

## Input
The module expects a pandas dataframe with reasonably named columns. Columns should either comprise the observed frequencies in a contingency table:

```python3
>>> df.head()
            item  O11    O12  O21     O22
1    appreciated    1  15333    1  176663
2        certain    7  15327  113  176551
3      measuring    1  15333    7  176657
4   particularly    2  15332   45  176619
5        arrived    2  15332    3  176661
```

or follow Evert's (2004: 36) notation of frequency signatures:

```python3
>>> df.head()
            item  f     f1   f2       N
1    appreciated  1  15334    2  191998
2        certain  7  15334  120  191998
3      measuring  1  15334    8  191998
4   particularly  2  15334   47  191998
5        arrived  2  15334    5  191998
```

Combinations of both are possible, but you should make sure that all of the following equations hold:

- f = O11
- f1 = O11 + O12
- f2 = O11 + O21
- N = O11 + O12 + O21 + O22

## Frequencies
Given a Dataframe as specified above, you can calculate expected frequencies via

```python3
>>> import association_measures.frequencies as fq

>>> # inplace operation
>>> fq.expected_frequencies(df)
>>> df.head()

            item       E11           E12         E21            E22       N ...
1    appreciated  0.159731  15333.840269    1.840269  176662.159731  191998 ...
2        certain  9.583850  15324.416150  110.416150  176553.583850  191998 ...
3      measuring  0.638923  15333.361077    7.361077  176656.638923  191998 ...
4   particularly  3.753675  15330.246325   43.246325  176620.753675  191998 ...
5        arrived  0.399327  15333.600673    4.600673  176659.399327  191998 ...

>>> # alternatively:
df['E11'], df['E12'], df['E21'], df['E22'] = fq.expected_frequencies(df, inplace=False)
```

## Association Measures

As of version 0.1.4, the following association measures are supported:

- z-score
- t-score
- dice
- log-likelihood
- mutual-information
- log-ratio

You can either calculate a specified measure:

```python3
>>> import association_measures.measures as am

>>> df['MI'] = am.mutual_information(df)
>>> df.head()

              l2  f     f1   f2       N        MI
1    appreciated  1  15334    2  191998  0.796611
2        certain  7  15334  120  191998 -0.136442
3      measuring  1  15334    8  191998  0.194551
4   particularly  2  15334   47  191998 -0.273427
5        arrived  2  15334    5  191998  0.699701
```

or calculate all available association measures (or a sub-set thereof):

```python3
>>> df = am.calculate_measures(df, inplace=False)
>>> am.calculate_measures(df, measures=['log_likelihood', 'log_ratio'], inplace=True)
```

NB: inplace operation will also add (and potentially over-write) columns for observed and expected frequencies.

# Development

The package is tested using pylint and pytest.

```bash
# Installing dev requirements
make install

# Compile Cython code
make compile

# Lint
make lint

# Unittest
make test

# Coverage
make coverage
```
