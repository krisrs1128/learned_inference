#' Functions for Simulating Image Parameters
#'
#' 2020-05-16 16:10:20
library("reshape2")
library("MASS")
library("ggplot2")

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
#' mprobs <- melt(probs, id.vars = c("Var1", "Var2"))
#' ggplot(mprobs) +
#'   geom_tile(aes(x = Var1, y = Var2, fill=value)) +
#'   facet_wrap(~variable)
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
    lambdas[, k] <- exp(-(betas_mat[, k] + processes[, k]))
  }

  probs <- t(apply(lambdas, 1, function(r) r / sum(r)))
  data.frame(x, probs)
}

#' Simulate an Inhomogeneous Poisson Process
#'
#' @examples
#' probs <- relative_intensities(x, 3, nu = 1)
#' intensity <- matern_process(x, 2)
#' z <- inhomogeous_process(500, intensity)
#' ggplot(intensity, aes(x = Var1, y = Var2, fill = z)) +
#'   geom_tile()
#' plot(z)
inhomogeous_process <- function(N0, intensity) {
  z <- matrix(runif(2 * N0), N0, 2)
  x <- as.matrix(intensity[, 1:2])

  sample_probs <- vector(length = N0)
  weight <- sum(exp(intensity$z))
  max_z <- max(intensity$z)
  for (i in seq_along(z)) {
    dists <- rowSums((x - z[i]) ^ 2)
    sample_probs[i] <- exp(intensity$z[which.min(dists)] - max_z)
  }

  z[which(rbinom(N0, 1, prob=sample_probs) == 1), ]
}
