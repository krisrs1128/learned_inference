
#' @export
features <- function(X, K = 2, sigma_e = 0.1) {
  N <- nrow(X)
  D <- nrow(X)
  svx <- svd(X)
  
  function(X) {
    Pi <- random_permutation(K)
    (X %*% svx$v[, 1:K] %*% diag(1/sqrt(svx$d[1:K])) + rmat(nrow(X), K, sigma_e)) %*% Pi
  }
}

#' @importFrom dplyr %>%
#' @export
supervised_features <- function(X, y, K = 2, sigma_e = 0.01) {
  N <- nrow(X)
  D <- nrow(X)
  svx <- svd(X)
  
  sigma_order <- cor(y, svx$u) %>%
    abs() %>%
    order(decreasing = TRUE)
  V <- svx$v[, sigma_order[1:K]]
  
  function(X) {
    Pi <- random_permutation(K)
    (X %*% V %*% diag(1/sqrt(svx$d[1:K])) + rmat(N, K, sigma_e)) %*% Pi
  }
}