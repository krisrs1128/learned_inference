#' Functions for Simulating Image Parameters
#'
#' 2020-05-16 16:10:20
library("reshape2")
library("MASS")
library("ggplot2")
library("dplyr")

#' Simulate from a Matern Process
#'
#' @examples
#' x <- expand.grid(seq(0.1, 1, 0.05), seq(0.1, 1, 0.05))
#' process_df <- matern_process(x, 1, 1)
#' ggplot(process_df) +
#'  geom_tile(aes(x = Var1, y = Var2, fill = z))
matern_process <- function(x, nu, alpha) {
  Sigma <- matern_kernel(x, nu, alpha)
  z <- mvrnorm(1, mu=rep(0, nrow(x)), Sigma)
  data.frame(x, z)
}

matern_kernel <- function(x, nu, alpha) {
  squared_dist <- dist(x) %>%
    as.matrix()

  Sigma <- (1/((2 ^ (nu - 1)) * gamma(nu))) *
    (squared_dist ^ nu) *
    besselK(squared_dist, nu)
  diag(Sigma) <- 1
  Sigma
}

#' Simulate Matern Probabilities
#'
#' @examples
#' library("reshape2")
#' x <- expand.grid(seq(0.1, 1, 0.05), seq(0.1, 1, 0.05))
#' probs <- relative_intensities(x, nu = 1)
#' @details #' See page 551 in SPATIAL AND SPATIO-TEMPORAL LOG-GAUSSIAN COX
#'   PROCESSES
relative_intensities <- function(x, K = 4, betas = NULL, ...) {
  if (is.null(betas)) {
    betas <- rnorm(K, 0, 0.5)
  }

  processes <- matrix(0, nrow(x), K)
  for (k in seq_len(K)) {
    processes[, k] <- matern_process(x, ...)[, 3]
  }

  lambdas <- matrix(0, nrow(x), K)
  betas_mat <- t(replicate(nrow(x), betas))
  for (k in seq_len(K)) {
    lambdas[, k] <- exp(betas_mat[, k] + processes[, k])
  }

  probs <- t(apply(lambdas, 1, function(r) r / sum(r)))
  data.frame(x, probs)
}

#' Simulate an Inhomogeneous Poisson Process
#'
#' We just thin out an ordinary poisson process.
inhomogeous_process <- function(N0, intensity) {
  z <- matrix(runif(2 * N0), N0, 2)
  x <- as.matrix(intensity[, 1:2])

  sample_probs <- vector(length = N0)
  max_z <- max(intensity$z)
  ixs <- vector(length = N0)

  for (i in seq_len(nrow(z))) {
    diffs <- x - t(replicate(nrow(x), z[i, ]))
    ixs[i] <- which.min(rowSums(diffs ^ 2))
    sample_probs[i] <- exp(intensity$z[ixs[i]] - max_z)
  }

  keep_ix <- which(rbinom(N0, 1, prob=sample_probs) == 1)
  z[keep_ix, ]
}

#' Mark an Inhomogeneous Poisson Process
mark_process <- function(z, probs, tau=1) {
  N <- nrow(z)
  marks <- vector(length = N)

  x <- as.matrix(probs[, 1:2])
  K <- ncol(probs) - 2

  for (i in seq_len(N)) {
    diffs <- x - t(replicate(nrow(x), z[i, ]))
    ix <- which.min(rowSums(diffs ^ 2))
    p <- unlist(probs[ix, 2:ncol(probs)])
    marks[i] <- rbinom(1, K - 1, p) # ignoring weighting for now
  }

  data.frame(z, mark = as.factor(1 + marks))
}
