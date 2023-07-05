# Performance
- performance is calculated on a Lenovo X1 Carbon (10th generation, i7)
- input data are 24,167 observations from [brown.csv](tests/data/brown.csv)
- we report  for 1000 iterations

## v0.2.7
- major performance improvement regarding conservative log-ratio with Poisson boundary (factor 50)
```
settings: iterations=1000, df_size=24167
-  0.0874 :: contingency_table
-  1.5254 :: expected_frequencies
-  0.1510 :: z_score
-  0.2906 :: t_score
-  1.7408 :: log_likelihood
-  0.6146 :: simple_ll
-  1.3270 :: min_sensitivity
-  0.2604 :: liddell
-  0.2502 :: dice
-  0.4494 :: log_ratio
-  4.6467 :: binomial_likelihood
-  2.1923 :: conservative_log_ratio
- 31.2882 :: conservative_log_ratio_poisson
-  0.3840 :: mutual_information
-  0.4441 :: local_mutual_information
```

## v0.2.6
```
Calculate contingency_table (iterations=1000, df_size=24168):         0.0873531000688672
Calculate expected_frequencies (iterations=1000, df_size=24168):      1.5203204130521044
Calculate z_score (iterations=1000, df_size=24168):                   0.14853612298611552
Calculate t_score (iterations=1000, df_size=24168):                   0.2881241790018976
Calculate log_likelihood (iterations=1000, df_size=24168):            1.7284309939714149
Calculate simple_ll (iterations=1000, df_size=24168):                 0.6111006899736822
Calculate min_sensitivity (iterations=1000, df_size=24168):           1.3227944150567055
Calculate liddell (iterations=1000, df_size=24168):                   0.25499376200605184
Calculate dice (iterations=1000, df_size=24168):                      0.2465739679755643
Calculate log_ratio (iterations=1000, df_size=24168):                 0.751795751042664
Calculate binomial_likelihood (iterations=1000, df_size=24168):       4.606213430990465
Calculate conservative_log_ratio (iterations=1000, df_size=24168):    2.2395021530101076
Calculate mutual_information (iterations=1000, df_size=24168):        0.3618475969415158
Calculate local_mutual_information (iterations=1000, df_size=24168):  0.41407940594945103
```
additionally:
- conservative log ratio with Poisson boundary: ~1.5s for 1 iteration
- hypergeometric likelihood: ~2.5s for 1 iteration
