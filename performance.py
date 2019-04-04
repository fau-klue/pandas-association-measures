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
code_1 = '''
df['O11'], df['O12'], df['O21'], df['O22'] = am.contingency_table(df)
'''

code_2 = '''
df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)
'''

code_3 = '''
df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)
df['am'] = am.z_score(df)
'''

code_4 = '''
df['E11'], df['E12'], df['E21'], df['E22'] = am.expected_frequencies(df)
df['am'] = am.mutual_information(df)
'''

res1 = timeit.timeit(setup=setup, stmt=code_1, number=iterations)
print('Calculate contingency_table (iterations={iter}): {res}'.format(iter=iterations, res=res1))
res2 = timeit.timeit(setup=setup, stmt=code_2, number=iterations)
print('Calculate expected_frequencies (iterations={iter}): {res}'.format(iter=iterations, res=res2))
res3 = timeit.timeit(setup=setup, stmt=code_3, number=iterations)
print('Calculate z_score (iterations={iter}): {res}'.format(iter=iterations, res=res3))
res4 = timeit.timeit(setup=setup, stmt=code_4, number=iterations)
print('Calculate MI (iterations={iter}): {res}'.format(iter=iterations, res=res4))
