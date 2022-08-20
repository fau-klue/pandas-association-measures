# preprocess cqpweb data
# convert to dataframe with columns
# lemma, f, f1, f2, N, lr, clr, lrc, lrc.normal, lrc.positive

# NB: keyword measures implemented below have different notation:
# f1 ~ O11 = f
# f2 ~ O12 = f1 - f
# N1 ~ C1 = f2
# N2 ~ C2 = N - f2

################################################################################
## Implementations of "standard" keyword measures (G2, log ratio)
##  - input are parallel vectors f1, f2 and parameters N1, N2
##  - at this point, we don't worry about scalability and accept large vector operations

## G2 = log-likelihood (using the standard AM form)
##  - if alpha is set, scores that are not significant at level alpha are set to 0
##  - with correct=TRUE, apply Bonferroni correction to specified significance level
G2.term <- function (O, E) {
  res <- O * log(O / E)
  res[O == 0] <- 0
  res
}
G2 <- function (f1, f2, N1, N2, length.f1=NULL, alpha=NULL, correct=TRUE) {
  stopifnot(length(f1) == length(f2))
  N <- N1 + N2
  R1 <- f1 + f2
  O11 <- f1; E11 <- R1 * N1 / N
  O12 <- f2; E12 <- R1 - E11
  O21 <- N1 - f1; E21 <- N1 - E11
  O22 <- N2 - f2; E22 <- N2 - E12
  G2 <- G2.term(O11, E11) + G2.term(O12, E12) + G2.term(O21, E21) + G2.term(O22, E22)
  res <- sign(O11 - E11) * 2 * G2
  if (!is.null(alpha)) {
    if (correct) {
      ifelse(length.f1, alpha <- alpha / length.f1, alpha <- alpha / length(f1))
    }
    theta <- qchisq(alpha, df=1, lower.tail=FALSE)
    res[G2 < theta / 2] <- 0 # the LLR statistic is 2 * G2
  }
  res
}

## Hardie's LogRatio according to CQPweb implementation
##  - if conv.level is set, compute conservative estimate (i.e. bdry of conf.int closer to zero)
##  - if correct=TRUE, apply Bonferroni correction to specified confidence level (Sidak is numerically unstable for large m)
##  - if poisson=TRUE, exact confidence intervals from a Poisson approximation are computed; required if there are cases of f2=0
##  - if alpha is set, scores are set to 0 if the difference is not significant according to a G2 test (with correct= as specified)
##  - following Hardie's implementation, we return log2 of relative risk, and replace cases of f2=0 with f2=0.5 (which is dubious)
LogRatio <- function (f1, f2, N1, N2, length.f1=NULL, conf.level=NULL, correct=TRUE, poisson=FALSE, alpha=NULL) {
  stopifnot(length(f1) == length(f2))
  stopifnot(all(f1 >= 1))
  f2.zero <- f2 == 0 # these cases need special handling
  f2.disc <- if (any(f2.zero)) f2 + 0.5 * f2.zero else f2 # questionable discounting according to Hardie (2014)
  if (!is.null(conf.level)) {
    alpha <- 1 - conf.level # desired significance level for two-sided conf.int
    if (correct) {
      ifelse(is.null(length.f1), alpha <- alpha / length(f1), alpha <- alpha / length.f1)
    }
    if (poisson) {
      ## exact conifdence interval based on Poisson approximation (Poisson rate = p with time base = n)
      lrr <- sapply(seq_along(f1), function (i) {
        res <- poisson.exact(c(f1[i], f2[i]), c(N1, N2), conf.level=(1 - alpha))
        if (f1[i] / N1 >= f2[i] / N2) max(0, log(res$conf.int[1])) else min(0, log(res$conf.int[2]))
      })
    } else {
      ## approximate confidence interval based on s.d. of log(rr), with Hardie's (2014) discounting
      z.factor <- -qnorm(alpha / 2) # number of s.d. for asymptotic two-sided conf.int
      lrr <- log((f1 / N1) / (f2.disc / N2))
      lrr.sd <- sqrt(1/f1 + 1/f2.disc - 1/N1 - 1/N2) # asymptotic s.d. of log(RR) according to Wikipedia
      # print(head(cbind(lrr / log(2), lrr.sd, z.factor)))
      lrr <- ifelse(lrr >= 0, 
                    pmax(lrr - z.factor * lrr.sd, 0), # log(RR) >= 0 -> lower bound of conf.int (clamped to >= 0)
                    pmin(lrr + z.factor * lrr.sd, 0)) # log(RR) < 0  -> upper bound of conf.int (clamped to <= 0)
    }
  }
  else {
    ## point estimate of log(rr)
    lrr <- log((f1 / N1) / (f2.disc / N2)) # questionable discounting according to Hardie (2014)
  }
  # if (!is.null(alpha)) {
  #   G2.scores <- G2(f1, f2, N1, N2, alpha=alpha, correct=correct)
  #   lrr[G2.scores == 0] <- 0 # set log(rr) to zero if difference is not significant
  # }
  lrr / log(2) # adjust to log2 units
}
################################################################################
# Evert 2022: Keyness @ DH
binom.confint <- function(k, n, conf.level=0.95, correct=FALSE,
                          alternative=c("two.sided", "less", "greater")) {
  alternative <- match.arg(alternative)
  stopifnot(all(k >= 0) && all(k <= n) && all(n >= 1))
  stopifnot(all(conf.level >= 0) && all(conf.level <= 1))
  
  ## significance level for underlying hypothesis test (with optional Bonferroni correction)
  alpha <- if (alternative == "two.sided") (1 - conf.level) / 2 else (1 - conf.level)
  if (correct) alpha <- alpha / length(k) # Bonferroni correction
  alpha <- rep_len(alpha, length(k))      # needs to be vector for safe.qbeta() 
  
  ## Clopper-Pearson method: invert binomial test (using incomplete Beta function)
  lower <- safe.qbeta(alpha, k, n - k + 1)
  upper <- safe.qbeta(alpha, k + 1, n - k, lower.tail=FALSE)
  switch(alternative,
         two.sided = data.frame(lower = lower, upper = upper),
         less      = data.frame(lower = 0,     upper = upper),
         greater   = data.frame(lower = lower, upper = 1))
}

## safely compute qbeta even for shape parameters alpha == 0 or beta == 0
safe.qbeta <- function (p, shape1, shape2, lower.tail=TRUE) {
  stopifnot(length(p) == length(shape1) && length(p) == length(shape2))
  is.0 <- shape1 <= 0
  is.1 <- shape2 <= 0
  ok <- !(is.0 | is.1)
  x <- numeric(length(p))
  x[ok] <- qbeta(p[ok], shape1[ok], shape2[ok], lower.tail=lower.tail) # shape parameters are valid
  x[is.0 & !is.1] <- 0 # density concentrated at x = 0 (for alpha == 0)
  x[is.1 & !is.0] <- 1 # density concentrated at x = 1 (for beta == 0)
  x[is.0 & is.1] <- NA # shouldn't happen in our case (alpha == beta == 0)
  x
}

LRC <- function (f1, f2, N1, N2, conf.level=.95, correct=TRUE) {
  stopifnot(length(f1) == length(f2))
  stopifnot(all(f1 + f2 >= 1))
  
  ## exact confidence interval from conditional Poisson test (two-sided)
  tau <- binom.confint(f1, f1 + f2, conf.level=conf.level, correct=correct, alternative="two.sided")
  ifelse(f1 / N1 >= f2 / N2, 
         pmax(log2( (N2 / N1) * tau$lower / (1 - tau$lower) ), 0),  # p1 >= p2 -> use lower bound (clamped to >= 0)
         pmin(log2( (N2 / N1) * tau$upper / (1 - tau$upper) ), 0))  # p1 < p2  -> use upper bound (clamped to <= 0)
}

PositiveLRC <- function (f1, f2, N1, N2, conf.level=.95, correct=TRUE) {
  stopifnot(length(f1) == length(f2))
  stopifnot(all(f1 + f2 >= 1))
  
  ## exact confidence interval from conditional Poisson test (one-sided)
  tau <- binom.confint(f1, f1 + f2, conf.level=conf.level, correct=correct, alternative="greater")
  log2( (N2 / N1) * tau$lower / (1 - tau$lower) )
}

ApproxLRC <- function (f1, f2, N1, N2, conf.level=.95, correct=TRUE) {
  stopifnot(length(f1) == length(f2))
  stopifnot(all(f1 >= 1))
  
  alpha <- 1 - conf.level                  # desired significance level 
  if (correct) alpha <- alpha / length(f1) # Bonferroni correction
  
  ## approximate confidence interval based on asymptotic standard deviation of log(rr)
  f2.disc <- pmax(f2, 0.5) #  with Hardie's (2014) questionable discounting
  lrr <- log((f1 / N1) / (f2.disc / N2))
  lrr.sd <- sqrt(1/f1 + 1/f2.disc - 1/N1 - 1/N2) # asymptotic s.d. of log(RR) according to Wikipedia
  z.factor <- -qnorm(alpha / 2)                  # number of s.d. for asymptotic two-sided conf.int
  lrr <- ifelse(lrr >= 0, 
                pmax(lrr - z.factor * lrr.sd, 0), # log(RR) >= 0 -> use lower bound (clamped to >= 0)
                pmin(lrr + z.factor * lrr.sd, 0)) # log(RR) < 0  -> use upper bound (clamped to <= 0)
  
  lrr / log(2) # adjust to log2 units
}

################################################################################

library(tidyverse)

# preprocess cqpweb data
# convert to dataframe with columns
# lemma
# f = O11
# f1 = R1
# f2 = C1
# N
# lr, lr2, clr

clr <- read_tsv("cqpweb-gold-clr.tsv", skip=3)
names(clr) <- c('rank', 'lemma', 'f2', 'E11', 'f', 'texts', 'clr')
lr <- read_tsv("cqpweb-gold-lr.tsv", skip=3)
names(lr) <- c('rank', 'lemma', 'f2', 'E11', 'f', 'texts', 'lr')
d <- left_join(clr[,-1], lr[, c("lemma", "lr")])

# additional numbers from CQPweb
N <- 19720567
length.f1 <- 13680

# calculate f1 using eq. E11 = f1 * f2 / N
f1 <- as.integer(mean(d$E11 / d$f2 * N))

# rename columns
res <- data.frame(lemma = d$lemma, 
                  f = d$f, 
                  f1 = f1, 
                  f2 = d$f2,
                  N = N,
                  lr.cqpweb = d$lr,
                  clr.cqpweb = d$clr)

# NB: keyword measures implemented above have different notation:
# f1 ~ O11 = f
# f2 ~ O21 = f2 - f
# N1 ~ R1 = f1
# N2 ~ R2 = N - f1

# Log Ratio #######################
res$lr <- LogRatio(
  f1 = res$f, f2 = res$f2 - res$f, N1 = res$f1, N2 = res$N - res$f1
)

# check that calculations of CQPweb and keyword measures are the same
plot(res$lr.cqpweb, res$lr)
abline(0, 1)
mean(round(res$lr.cqpweb, 1) == round(res$lr, 1), na.rm = T)
res[round(res$lr.cqpweb, 2) != round(res$lr, 2),] %>% drop_na() %>%
  select(c(lr.cqpweb, lr)) %>% round(2)
table(is.na(res$lr.cqpweb), is.na(res$lr))
# quasi-identical, lr.cqpweb has fewer calculations (filtered)

# Conservative Log Ratio ###########
res$clr <- LogRatio(
  f1 = res$f, f2 = res$f2 - res$f, N1 = res$f1, N2 = res$N - res$f1,
  length.f1 = length.f1, conf.level = .95
)

# check that calculations of CQPweb and keyword measures are the same
plot(res$clr.cqpweb, res$clr)
table(is.na(res$clr.cqpweb), is.na(res$clr))
abline(0, 1)
mean(round(res$clr.cqpweb, 1) == round(res$clr, 1), na.rm = T)
res[round(res$clr.cqpweb, 2) != round(res$clr, 2),] %>% drop_na() %>%
  select(c(clr.cqpweb, clr)) %>% round(2)
# no NAs
# quasi-identical
# - measures implemented here cut off at 0 (which is reasonable)
# - maybe f1 is off?

# to make the data set reproducible, we re-calculate conservative log-ratio here 
# neglecting real f1.length (number of types in w(node))
res$clr <- LogRatio(
  f1 = res$f, f2 = res$f2 - res$f, N1 = res$f1, N2 = res$N - res$f1,
  length.f1 = NULL, conf.level = .99
)

# "new" measures / implementations from DH
res <- res %>% mutate(
  lrc = LRC(f1 = f, f2 = f2 - f, N1 = f1, N2 = N - f1),
  lrc.positive = PositiveLRC(f1 = f, f2 = f2 - f, N1 = f1, N2 = N - f1),
  lrc.normal = ApproxLRC(f1 = f, f2 = f2 - f, N1 = f1, N2 = N - f1),
)

res %>%
  select(-c("lr.cqpweb", "clr.cqpweb")) %>%
  write_tsv("log-ratio-gold.tsv")
