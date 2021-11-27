
#' @export
param_boot <- function(u_hat, d_hat, E) {
  eB <- matrix(sample(E, replace = TRUE), nrow(E), ncol(E))
  Pi <- random_permutation(ncol(E))
  Zb <- (u_hat %*% diag(sqrt(d_hat)) + eB) %*% Pi
  list(Zb = Zb, ub = svd(Zb)$u %*% diag(sqrt(svd(Zb)$d)))
}

#' @export
param_boot_ft <- function(u_hat, d_hat, Eb) {
  Estar <- do.call(cbind, Eb)
  K <- length(d_hat)
  Estar <- as.matrix(Estar[, sample(ncol(Estar), K, replace = T)])
  Pi <- random_permutation(K)
  Zb <- (u_hat %*% diag(sqrt(d_hat)) + Estar) %*% Pi
  list(Zb = Zb, ub = svd(Zb)$u %*% diag(sqrt(svd(Zb)$d)))
}

#' @importFrom purrr map
#' @export
arr_to_list <- function(x, df = F) {
  if (df) {
    res <- map(1:dim(x)[3], ~ data.frame(x[,, .]))
  } else {
    res <- map(1:dim(x)[3], ~ x[,, .])
  }
  
  res
}

#' @export
procrustes <- function(x_list, tol = 0.05) {
  x_align <- array(dim = c(dim(x_list[[1]]), length(x_list)))
  M <- x_list[[1]]

  while (TRUE) {
    # solve each problem
    for (i in seq_along(x_list)) {
      svd_i <- svd(t(x_list[[i]]) %*% M)
      beta <- sum(svd_i$d) / sum(x_list[[i]] ^ 2)
      x_align[,, i] <- beta * x_list[[i]] %*% svd_i$u %*% t(svd_i$v)
    }

    # new procrustes mean
    M_old <- M
    M <- apply(x_align, c(1, 2), mean)
    coord_change <- mean(abs(M - M_old))
    if (coord_change < tol) break
  }

  list(x_align = x_align, M = M)
}
