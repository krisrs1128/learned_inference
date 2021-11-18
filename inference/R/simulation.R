
factor_model <- function(N, D, K, S) {
  
}

rmat <- function(N, D, sd=1) {
  matrix(rnorm(N * D, sd = sd), N, D)
}

random_permutation <- function(K) {
  pi <- sample(K)
  pi_mat <- matrix(0, K, K)
  for (k in seq_len(K)) {
    pi_mat[k, pi[k]] <- 1
  }
  
  pi_mat
}

factor_terms <- function(N, D, K, feature_variances=1) {
  list(L = rmat(N, K, feature_variances), V = rmat(D, K))
}

sparse_factor_terms <- function(N, D, K, feature_variances = 1, 
                                delta_mass = 0.2) {
  terms <- factor_terms(N, D, K, feature_variances)
  n_entries <- length(terms$L)
  terms$L[sample(n_entries, n_entries * delta_mass)] <- 0
  terms
}

factor_model <- function(N, D, K, mode = "sparse", sigma = 1, 
                         feature_variances = 1, delta_mass = 0.2) {
  if (mode == "sparse") {
    terms <- sparse_factor_terms(N, D, K, feature_variances, delta_mass)
  } else {
    terms <- factor_terms(N, D, K, feature_variances)
  }
  
  Pi <- random_permutation(K)
  Z <- terms$L %*% Pi %*% t(terms$V %*% Pi) + rmat(N, D, sigma)
  list(L = terms$L, V = terms$V, Z = Z)
}

simulate_response <- function(L, S, sigma_beta = 1, sigma_y = 1) {
  beta <- vector(length = K)
  beta[sample(K, S)] <- rnorm(S, sd = sigma_beta)
  y <- L %*% beta + rnorm(nrow(L), sd = sigma_y)
  list(beta = beta, y = y)
}

svd_extractor <- function(Z, K_hat = 5) {
  sv_z <- svd(Z)
  function (x_star) {
    x_star %*% sv_z$v[, 1:K_hat]
  }
}

sca_extractor <- function(Z, K_hat = 5) {
  library(epca)
  sc_z <- sca(Z, k = K_hat)
  function (x_star) {
    x_star %*% sc_z$loadings
  }
}

zero_relatedness <- function(L, L_hat, beta, beta_hat) {
  scores <- abs(t(L_hat) %*% L) * beta_hat
  s0 <- which(beta == 0)
  weights <- scores[s0, ]
  list(score = rowSums(weights), weights = weights)
}

eta_relatedness <- function(L, L_hat, beta, beta_hat) {
  rowSums(t(L_hat) %*% L %*% diag(beta))
}