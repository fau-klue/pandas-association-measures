"""
Script to measure the performance
"""

import timeit
import sys

# Number of iterations
iterations = 1000
if len(sys.argv) > 1:
    iterations = int(sys.argv[1])

# code snippet to be executed only once
setup = """
import pandas as pd
import numpy as np
import association.measures as am

df = pd.DataFrame({'f1': np.random.randint(100, size=10),
                   'f2': np.random.randint(100, size=10),
                   'O11': np.random.randint(100, size=10),
                   'N': [100] * 10})

df['O11'], df['O12'], df['O21'], df['O22'] = am.contingency_table(df)
"""

# code snippet whose execution time is to be measured
codes = [
    {
    'name': 'contingency_table',
    'code': '''
df['O11'], df['O12'], df['O21'], df['O22'] = am.contingency_table(df)
    '''
    },
    {
    'name': 'expected_frequencies',
    'code': '''
df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)
    '''
    },
    {
    'name': 'z_score',
    'code': '''
df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)
df['am'] = am.z_score(df)
    '''
    },
    {
    'name': 'mutual_information',
    'code': '''
df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)
df['am'] = am.mutual_information(df)
    '''
    },
]

for code in codes:
    res = timeit.timeit(setup=setup, stmt=code['code'], number=iterations)
    print('Calculate {func} (iterations={iter}, df_size={size}): {res}'.format(iter=iterations, size=10, res=res, func=code['name']))
