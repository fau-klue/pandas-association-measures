library(tidyverse)
library(gespeR)

#' Calculate average overlap (RBO) between two profiles
overlap.pairwise <- function(table1, table2, col_item = "item", col_score = "score", p = .95, k = 50){
  
  left.list <- table1 |> tibble() |> pull(col_score)
  names(left.list) <- table1 |> tibble() |> pull(col_item)

  right.list <- table2 |> tibble() |> pull(col_score)
  names(right.list) <- table2 |> tibble() |> pull(col_item)
  
  # calculate rbo
  value <- rbo(left.list, right.list, p, k)
  
  return(value)
}

d <- read_tsv("log-ratio-gold.tsv")
d1 <- d |> select(lemma, lrc.positive) |> rename(score = lrc.positive, item = lemma) |> arrange(desc(score)) |>  head(50)
d2 <- d |> select(lemma, lrc.normal) |> rename(score = lrc.normal, item = lemma) |> arrange(desc(score)) |> head(50)

rbos <- tibble()
for (p_ in (1:10) / 10){
  for (k_ in (1:10) * 5){
    rbos <- rbind(rbos, tibble(p = p_, k = k_, rbo = overlap.pairwise(d1, d2, p = p_, k = k_)))
  }
}

rbos |> write_tsv("rbo.tsv")

