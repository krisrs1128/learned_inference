
#' @param z_list A list of feature data frames.
#'
#' @export
pairwise_rv <- function(z_list) {
  B <- length(z_list)

  rv_mat <- matrix(0, nrow = B, ncol = B)
  for (i in seq_len(B)) {
    print(i)
    for (j in seq_len(i - 1)) {
      rv_mat[i, j] <- coefficientRV(z_list[[i]], z_list[[j]])
    }
  }
  rv_mat + t(rv_mat)
}

#' Reorganized version from
#' https://rdrr.io/cran/FactoMineR/src/R/coeffRV.R
coefficientRV <- function(X, Y) {
  Y <- scale(Y, scale = FALSE)
  X <- scale(X, scale = FALSE)
  W1 <- t(X) %*% X
  W2 <- t(Y) %*% Y
  W3 <- t(X) %*% Y
  W4 <- t(Y) %*% X
  tr <- function(X) { sum(diag(X)) }
  tr(W3 %*% W4) / (tr(W1 %*% W1) * tr(W2 %*% W2)) ^ 0.5
}

svds <- function(x_list, ...) {
  results <- list()
  for (i in seq_along(x_list)) {
    svd_res <- irlba(x_list[[i]], ...)
    results[[i]] <- list(u = svd_res$u, d = svd_res$d)
  }
  
  results
}