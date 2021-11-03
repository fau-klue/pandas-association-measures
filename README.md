[![Build Status](https://github.com/fau-klue/pandas-association-measures/actions/workflows/python-build.yml/badge.svg)](https://github.com/fau-klue/pandas-association-measures/actions/workflows/python-build.yml)
[![Coverage Status](https://coveralls.io/repos/github/fau-klue/pandas-association-measures/badge.svg?branch=master)](https://coveralls.io/github/fau-klue/pandas-association-measures?branch=master)

# Statistical Association Measures for Python pandas

> Association measures are mathematical formulae that interpret cooccurrence frequency data. For each pair of words extracted from a corpus, they compute an association score, a single real value that indicates the amount of (statistical) association between the two words.

http://www.collocations.de/AM/index.html

# Installation

**Prerequisites:**
- [pandas](https://pandas.pydata.org/)
- [scipy](https://scipy.org/) (as of version v0.1.7)

**Installation using pip:**

    pip install association-measures

**Installation from source (requires Cython):**

    # Compile Cython code
    python setup.py build_ext --inplace

    # Cython already compiled
    python setup.py install

# Usage

## Input
The module expects a pandas dataframe with reasonably named columns. Columns should either comprise the observed frequencies in a contingency table:

```python3
>>> df.head()
            item  O11    O12  O21     O22
id
1    appreciated    1  15333    1  176663
2        certain    7  15327  113  176551
3      measuring    1  15333    7  176657
4   particularly    2  15332   45  176619
5        arrived    2  15332    3  176661
```

or follow [Evert's (2008: Figure 8)](https://www.stefan-evert.de/PUB/Evert2007HSK_extended_manuscript.pdf) notation of frequency signatures:

```python3
>>> df.head()
            item  f     f1   f2       N
id
1    appreciated  1  15334    2  191998
2        certain  7  15334  120  191998
3      measuring  1  15334    8  191998
4   particularly  2  15334   47  191998
5        arrived  2  15334    5  191998
```

Combinations of both are possible, but you should make sure to include four independent values, and that all of the following equations hold:

- f = O11
- f1 = O11 + O12
- f2 = O11 + O21
- N = O11 + O12 + O21 + O22

## Frequencies
Given a dataframe as specified above, you can calculate expected frequencies via

```python3
>>> import association_measures.frequencies as fq
>>> df_exp = fq.expected_frequencies(df)
>>> df_exp.head()
         E11           E12         E21            E22
1   0.159731  15333.840269    1.840269  176662.159731
2   9.583850  15324.416150  110.416150  176553.583850
3   0.638923  15333.361077    7.361077  176656.638923
4   3.753675  15330.246325   43.246325  176620.753675
5   0.399327  15333.600673    4.600673  176659.399327
```

The `observed_frequency` method will convert to contingency notation:

```python3
>>> import association_measures.frequencies as fq
>>> df_obs = fq.observed_frequencies(df)
>>> df_obs.head()
    O11    O12  O21     O22
id
1     1  15333    1  176663
2     7  15327  113  176551
3     1  15333    7  176657
4     2  15332   45  176619
5     2  15332    3  176661
```

Note that all methods return dataframes that are indexed the same way the input dataframe is indexed:

```python3
>>> df.head()
              f     f1   f2       N
item
appreciated   1  15334    2  191998
certain       7  15334  120  191998
measuring     1  15334    8  191998
particularly  2  15334   47  191998
arrived       2  15334    5  191998
>>> fq.observed_frequencies(df)
              O11    O12  O21     O22
item
appreciated     1  15333    1  176663
certain         7  15327  113  176551
measuring       1  15333    7  176657
particularly    2  15332   45  176619
arrived         2  15332    3  176661
```

You can thus `join` the results directly to the input.


## Association Measures

As of version 0.1.7, the following association measures are supported:

- asymptotic hypothesis tests:
  - z-score (`z_score`)
  - t-score (`t_score`)
  - log-likelihood (`log_likelihood`)
  - simple-ll (`simple_ll`)
- point estimates of association strength:
  - log-ratio (`log_ratio`)
  - Dice coefficient (`dice`)
- information theory:
  - mutual information (`mutual_information`)
  - local MI (`local_mutual_information`)
- conservative estimates:
  - conservative log-ratio (`conservative_log_ratio`)

You can either calculate specific measures:

```python3
>>> import association_measures.measures as am
>>> df_am = am.calculate_measures(df, measures=['log_likelihood', 'log_ratio'])
>>> df_am.head()
    log_likelihood  log_ratio
1         2.448757   3.526202
2        -0.829802  -0.486622
3         0.191806   0.718847
4        -1.059386  -0.965651
5         3.879126   2.941240
```

or calculate all available measures:

```python3
>>> df = am.calculate_measures(df)
>>> df_am.head()
               z_score   t_score  log_likelihood  simple_ll      dice  log_ratio  mutual_information  local_mutual_information  conservative_log_ratio
item
appreciated   2.102442  0.840269        2.448757   1.987992  0.000130   3.526202            0.796611                  0.796611                     0.0
certain      -0.834636 -0.976603       -0.829802  -0.769331  0.000906  -0.486622           -0.136442                 -0.955094                     0.0
measuring     0.451726  0.361077        0.191806   0.173788  0.000130   0.718847            0.194551                  0.194551                     0.0
particularly -0.905150 -1.240035       -1.059386  -0.988997  0.000260  -0.965651           -0.273427                 -0.546853                     0.0
arrived       2.533018  1.131847        3.879126   3.243141  0.000261   2.941240            0.699701                  1.399402                     0.0
```

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
