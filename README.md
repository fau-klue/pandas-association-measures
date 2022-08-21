[![Build Status](https://github.com/fau-klue/pandas-association-measures/actions/workflows/python-build.yml/badge.svg)](https://github.com/fau-klue/pandas-association-measures/actions/workflows/python-build.yml)
[![PyPI version](https://badge.fury.io/py/association-measures.svg)](https://badge.fury.io/py/association-measures)
[![License](https://img.shields.io/pypi/l/association-measures.svg)](https://github.com/fau-klue/association-measures/blob/master/LICENSE)
[![Imports: pandas](https://img.shields.io/badge/%20imports-pandas-%231674b1?style=flat&labelColor=gray)](https://pandas.pydata.org/)
<!-- [![Coverage Status](https://coveralls.io/repos/github/fau-klue/pandas-association-measures/badge.svg?branch=master)](https://coveralls.io/github/fau-klue/pandas-association-measures?branch=master) -->

# Statistical Association Measures for Python pandas

> Association measures are mathematical formulae that interpret cooccurrence frequency data. For each pair of words extracted from a corpus, they compute an association score, a single real value that indicates the amount of (statistical) association between the two words.

http://www.collocations.de/AM/index.html

# Installation

##### Dependencies
- [pandas](https://pandas.pydata.org/)
- [scipy](https://scipy.org/)

##### Installation using pip

    python3 -m pip install association-measures

##### Installation from source (requires Cython)

    # Compile Cython code
    python3 setup.py build_ext --inplace

    # Cython already compiled
    python3 setup.py install

# Usage

## Input

The module expects a pandas dataframe with reasonably named columns; i.e. the columns must follow one of the following notations:

### contingency table
```python3
>>> df
            item  O11    O12  O21     O22
1    appreciated    1  15333    1  176663
2        certain    7  15327  113  176551
3      measuring    1  15333    7  176657
4   particularly    2  15332   45  176619
5        arrived    2  15332    3  176661
```

### frequency signature (see [Evert 2008: Figure 8](https://www.stephanie-evert.de/PUB/Evert2007HSK_extended_manuscript.pdf))
```python3
>>> df
            item  f     f1   f2       N
1    appreciated  1  15334    2  191998
2        certain  7  15334  120  191998
3      measuring  1  15334    8  191998
4   particularly  2  15334   47  191998
5        arrived  2  15334    5  191998
```
where `f=O11`, `f1=O11+O12`, `f2=O11+O21`, `N=O11+O12+O21+O22`.

### corpus frequencies (“keyword-friendly”)
```python3
>>> df
            item  f1     N1   f2      N2
1    appreciated   1  15334    1  176664
2        certain   7  15334  113  176664
3      measuring   1  15334    7  176664
4   particularly   2  15334   45  176664
5        arrived   2  15334    3  176664
```
where `f1=O11`, `f2=O21`, `N1=O11+O12`, `N2=O21+O22`.

## Observed and Expected Frequencies
Given a dataframe following one of the notations specified above, you can calculate expected frequencies via

```python3
>>> import association_measures.frequencies as fq
>>> fq.expected_frequencies(df)
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
>>> fq.observed_frequencies(df)
    O11    O12  O21     O22
1     1  15333    1  176663
2     7  15327  113  176551
3     1  15333    7  176657
4     2  15332   45  176619
5     2  15332    3  176661
```

Note that all methods return dataframes that are indexed the same way the input dataframe is indexed:

```python3
>>> df
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

The following association measures are currently implemented (v0.2.2):

- asymptotic hypothesis tests:
  - **z-score** (`z_score`)
  - **t-score** (`t_score`)
    - parameter: `disc`
  - **Dunning's log-likelihood ratio** (`log_likelihood`)
    - parameter: `signed`
  - **simple-ll** (`simple_ll`)
    - parameter: `signed`
- point estimates of association strength:
  - **Liddell** (`liddell`)
  - **minimum sensitivity** (`min_sensitivity`)
  - [**log-ratio**](http://cass.lancs.ac.uk/log-ratio-an-informal-introduction/) (`log_ratio`)
    - parameter: `disc`
  - **Dice coefficient** (`dice`)
- information theory:
  - **mutual information** (`mutual_information`)
      - parameter: `disc`
  - **local mutual information** (`local_mutual_information`)
- conservative estimates
  - [**conservative log-ratio**](https://osf.io/cy6mw/) (`conservative_log_ratio`)
    - parameters: `disc`, `alpha`, `correct`, `one_sided`, `boundary`, `vocab`

You can either calculate specific measures:

```python3
>>> import association_measures.measures as am
>>> am.log_likelihood(df)
item
appreciated      2.448757
certain         -0.829802
measuring        0.191806
particularly    -1.059386
arrived          3.879126
```

This assumes that `df` contains the necessary columns (observed frequencies in contingency notation and expected frequencies).  In most cases, it is most convenient to just use `score()`:

```python3
>>> import association_measures.measures as am
>>> am.score(df, measures=['log_likelihood'])
              O11    O12  O21     O22     R1      R2   C1      C2       N       E11           E12         E21            E22  log_likelihood         ipm  ipm_reference  ipm_expected
item                                                                                                                                                                                 
appreciated     1  15333    1  176663  15334  176664    2  191996  191998  0.159731  15333.840269    1.840269  176662.159731        2.448757   65.214556       5.660463     10.416775
certain         7  15327  113  176551  15334  176664  120  191878  191998  9.583850  15324.416150  110.416150  176553.583850       -0.829802  456.501891     639.632296    625.006510
measuring       1  15333    7  176657  15334  176664    8  191990  191998  0.638923  15333.361077    7.361077  176656.638923        0.191806   65.214556      39.623240     41.667101
particularly    2  15332   45  176619  15334  176664   47  191951  191998  3.753675  15330.246325   43.246325  176620.753675       -1.059386  130.429112     254.720826    244.794217
arrived         2  15332    3  176661  15334  176664    5  191993  191998  0.399327  15333.600673    4.600673  176659.399327        3.879126  130.429112      16.981388     26.041938
```

Note that by default, `score()` yields observed frequencies in contingency notation (and marginal frequencies) as well as expected frequencies. You can turn off this behaviour setting `freq=False`.

To calculate all available measures, don't specify any measures:

```python3
>>> am.score(df, freq=False)
               z_score   t_score  log_likelihood  simple_ll  min_sensitivity   liddell      dice  log_ratio  binomial_likelihood  conservative_log_ratio  mutual_information  local_mutual_information
item
appreciated   2.102442  0.840269        2.448757   1.987992         0.000065  0.420139  0.000130   3.526202             0.000000                     0.0            0.796611                  0.796611
certain      -0.834636 -0.976603       -0.829802  -0.769331         0.000457 -0.021546  0.000906  -0.486622             0.117117                     0.0           -0.136442                 -0.955094
measuring     0.451726  0.361077        0.191806   0.173788         0.000065  0.045136  0.000130   0.718847             0.000000                     0.0            0.194551                  0.194551
particularly -0.905150 -1.240035       -1.059386  -0.988997         0.000130 -0.037321  0.000260  -0.965651             0.224042                     0.0           -0.273427                 -0.546853
arrived       2.533018  1.131847        3.879126   3.243141         0.000130  0.320143  0.000261   2.941240             0.000000                     0.0            0.699701                  1.399402
```

You can also pass constant integer counts as parameters to `score()`.  This is reasonable for the following notations:

- frequency signature: integers `f1` and `N` (DataFrame contains columns `f` and `f2`)
  ```python3
  >>> df
                f   f2
  item
  appreciated   1    2
  certain       7  120
  measuring     1    8
  particularly  2   47
  arrived       2    5
  >>> am.score(df, f1=15334, N=191998)
  ```

- corpus frequencies: integers `N1` and `N2` (DataFrame contains columns `f1` and `f2`)
  ```python3
  >>> df
                f1   f2
  item
  appreciated    1    1
  certain        7  113
  measuring      1    7
  particularly   2   45
  arrived        2    3
  >>> am.score(df, N1=15334, N2=176664)
  ```

Some association measures have parameters (see above). You can pass these parameters as keywords to `score()`, e.g.:
```python3
>>> am.score(df, measures=['log_likelihood'], signed=False, freq=False)
              log_likelihood
item
appreciated         2.448757
certain             0.829802
measuring           0.191806
particularly        1.059386
arrived             3.879126
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

# Performance
make performance
```
