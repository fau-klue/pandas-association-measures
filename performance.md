# Performance
- performance is calculated on a Lenovo X1 Carbon (10th generation, i7)
- input data are 24,167 observations from [brown.csv](tests/data/brown.csv)
- NB: dataframe contains 4241 duplicated frequency signatures (for which calculation will only be run once since v0.2.7)
- for each measure, we report time needed for 1000 scorings of the whole dataframe

## v0.2.7
- major performance improvement regarding conservative log-ratio with Poisson boundary (factor 50)
```
settings: iterations=1000, df_size=24167
-  0.0871 :: contingency_table
-  1.5258 :: expected_frequencies
-  0.1507 :: z_score
-  0.2899 :: t_score
-  1.7406 :: log_likelihood
-  0.6125 :: simple_ll
-  1.2981 :: min_sensitivity
-  0.2584 :: liddell
-  0.2491 :: dice
-  0.4460 :: log_ratio
-  4.5788 :: binomial_likelihood
-  2.1891 :: conservative_log_ratio
- 29.8616 :: conservative_log_ratio_poisson
-  0.3702 :: mutual_information
-  0.4314 :: local_mutual_information
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
