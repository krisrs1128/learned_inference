
#' @importFrom glmnet glmnet
#' @export
stability_selection <- function(X, y, B = 1000) {
  n <- nrow(X)
  p <- ncol(X)
  coef_paths <- array(dim = c(p, n_lambda, B))
  for (b in seq_len(B)) {
    ix <- sample(seq_len(n), n / 2, replace = FALSE)
    fit <- glmnet(X[ix, ], y[ix])
    coef_paths[, , b] <- coef(fit)
  }

  Pi <- apply(coef_paths, 3, function(z) abs(z) > 0)
  list(Pi = Pi, coef_paths = coef_paths)
}

#' @importFrom reshape2 melt
#' @export
melt_stability <- function(res) {
  mpi <- melt(res$Pi, varnames = c("j", "lambda"))
  mcoef_paths <- melt(res$coef_paths, varnames = c("j", "lambda", "b"))
  list(Pi = mpi, coef_paths = mcoef_paths)
}

#' @importFrom reticulate import
#' @export
read_acts <- function(paths) {
  results <- list()
  np <- import("numpy")
  for (i in seq_along(paths)) {
    system(sprintf("tar -zxvf %s", paths[i]))
    results[[i]] <- np$load(upath)  # how to get path to unzipped?
  }

  results
}
