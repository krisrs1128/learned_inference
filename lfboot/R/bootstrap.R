
#' @export
param_boot <- function(Z, K = 2) {
  svz <- svd(Z)
  u_hat <- svz$u[, 1:K]
  d_hat <- svz$d[1:K]
  v_hat <- svz$v[, 1:K]
  E <- Z - u_hat %*% diag(sqrt(d_hat)) %*% t(v_hat)

  function() {
    param_boot_(u_hat, d_hat, E)
  }
}

#' Zb here is like the Lb used in the writeup
#' @export
param_boot_ <- function(u_hat, d_hat, E) {
  eB <- matrix(sample(E, nrow(E) * length(d_hat), replace = TRUE), nrow(E), length(d_hat))
  Pi <- random_permutation(length(d_hat))
  Zb <- (u_hat %*% diag(sqrt(d_hat)) + eB) %*% Pi
  list(Zb = Zb, ub = svd(Zb)$u %*% diag(sqrt(svd(Zb)$d)))
}

#' Zb here is like the Lb used in the writeup
#' @export
param_boot_ft <- function(Zb, K = 2) {
  ud_hats <- procrustes(Zb)$x_align %>%
    apply(c(1, 2), mean)
  
  svz <- svd(ud_hats)
  u_hat <- svz$u[, 1:K]
  d_hat <- svz$d[1:K]
  v_hat <- svz$v[, 1:K]
  Eb <- map(Zb, ~ . - u_hat %*% diag(sqrt(d_hat)) %*% t(v_hat))
  
  function() {
    param_boot_ft_(u_hat, d_hat, Eb)
  }
}
  
#' @export
param_boot_ft_ <- function(u_hat, d_hat, Eb) {
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

#' @importFrom expm sqrtm
#' @export
within_ellipse <- function(x, new_point, level = 0.95) {
  params <- cov.wt(x)
  new_point_ <- solve(sqrtm(params$cov)) %*% (new_point - params$center)
  sum(new_point_ ^ 2) < sqrt(2 * qf(level, 2, 2))
}

#' @importFrom dplyr %>% select
#' @importFrom purrr map map2_dbl
#' @export
coverage <- function(samples, centers, level = 0.95) {
  samples <- samples %>%
    split(.$i) %>%
    map(~ as.matrix(select(., X1, X2)))
  
  centers <- centers %>%
    split(.$i) %>%
    map(~ unlist(select(., X1, X2)))
    
  map2_dbl(samples, centers, ~ within_ellipse(.x, .y, level = level))
}
