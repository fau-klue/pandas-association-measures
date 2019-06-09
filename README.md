[![Build Status](https://travis-ci.org/fau-klue/pandas-association-measures.svg?branch=master)](https://travis-ci.org/fau-klue/pandas-association-measures)
[![Coverage Status](https://coveralls.io/repos/github/fau-klue/pandas-association-measures/badge.svg?branch=master)](https://coveralls.io/github/fau-klue/pandas-association-measures?branch=master)

# Corpus Association Measures for Python pandas

> Association measures are mathematical formulae that interpret cooccurrence frequency data. For each pair of words extracted from a corpus, they compute an association score, a single real value g that indicates the amount of (statistical) association between the two words.

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

```bash
# Expected DataFrame:

>>> df.head()
   Unnamed: word    O11 f1     f2         N
0           We      8   75  45473  909768.0
1           are     6   75  17987  909768.0
2           the     18  75  35499  909768.0
3           Knights 5   54  45473  909768.0
4           who     15  54  35499  909768.0
5           say     7   159    43  909768.0
```

Calculations:

```python
import association_measures.frequencies as fq
import association_measures.measures as am

# Create the contigency table with the observed frequencies:
df['O11'], df['O12'], df['O21'], df['O22'] = fq.observed_frequencies(df)

# Create the contigency table with the expected frequencies:
df['E11'], df['E12'], df['E21'], df['E22'] = fq.expected_frequencies(df)

# Calculate an association measure:
df['am'] = am.mutual_information(df)

# Calculate all association measure:
df = am.calculate_measures(df)
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
