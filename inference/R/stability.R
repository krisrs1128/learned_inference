
#' @export
subset_matrices <- function(rdata, cols = as.character(1:40)) {
  X <- rdata %>%
    select(cols) %>%
    as.matrix()

  y <- rdata %>%
    .[["y"]]

  list(X = X, y = y)
}

#' @importFrom glmnet glmnet
#' @export
stability_selection <- function(X, y, B = 1000, lambda) {
  n <- nrow(X)
  p <- ncol(X)
  coef_paths <- array(dim = c(p + 1, length(lambda), B))
  for (b in seq_len(B)) {
    ix <- sample(seq_len(n), n / 2, replace = FALSE)
    fit <- glmnet(X[ix, ], y[ix], lambda = lambda)
    coef_paths[, , b] <- as.matrix(coef(fit))
  }

  Pi <- apply(coef_paths, c(1, 2), function(z) mean(abs(z) > 0))
  list(Pi = Pi, coef_paths = coef_paths)
}

#' @importFrom reshape2 melt
#' @export
melt_stability <- function(res) {
  mpi <- melt(res$Pi, varnames = c("j", "lambda"))
  mcoef_paths <- melt(res$coef_paths, varnames = c("j", "lambda", "b"))
  list(Pi = mpi, coef_paths = mcoef_paths)
}

#' @export
untar_all <- function(paths, data_dir = ".") {
  for (i in seq_along(paths)) {
    exdir <- file.path(data_dir, tools::file_path_sans_ext(basename(paths[[i]])))
    if (!dir.exists(exdir)) {
      untar(paths[i], exdir = exdir)
    }
  }
}

#' @importFrom reticulate import
#' @export
read_npys <- function(paths, data_dir = ".") {
  results <- list()
  np <- import("numpy")
  for (f in paths) {
    results[[f]] <- np$load(f)
  }
  results
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

    #print(coord_change)
    if (coord_change < tol) break
  }

  list(x_align = x_align, M = M)
}

#' Plot a Grid of Images
#'
#' @examples
#' paths <- list.files("~/Documents/stability_data/tiles/", full = TRUE)
#' coordinates <- matrix(rnorm(2 * length(paths)), length(paths), 2)
#' coordinates <- data.frame(coordinates)
#' colnames(coordinates) <- c("x", "y")
#' image_grid(coordinates, paths)
#'
#' @importFrom pdist pdist
#' @importFrom reticulate import
#' @importFrom ggplot2 ggplot geom_point aes coord_fixed theme_bw
#'   annotation_raster %+%
#' @export
image_grid <- function(coordinates, paths, density = c(15, 15), min_dist=0.1, imsize = 0.2) {
  if (length(density) == 1) {
    density <- c(density, density)
  }
  
  np <- import("numpy")
  p <- ggplot() +
    coord_fixed() +
    theme(legend.position = "none") +
    scale_fill_brewer(palette = "Set3")
  
  # get distances between anchor points and scores
  x_range <- c(min(coordinates$x), max(coordinates$x))
  y_range <- c(min(coordinates$y), max(coordinates$y))
  x_grid <- seq(x_range[1], x_range[2], length.out = density[1])
  y_grid <- seq(y_range[1], y_range[2], length.out = density[2])
  xy_grid <- expand.grid(x_grid, y_grid)
  dists <- as.matrix(pdist(xy_grid, as.matrix(coordinates)))
  
  # overlay the closest points
  used_ix <- c()
  for (i in seq_len(nrow(dists))) {
    min_ix <- which.min(dists[i, ])
    if (dists[i, min_ix] > min_dist) next
    if (min_ix %in% used_ix) next
    used_ix <- c(used_ix, min_ix)
    
    im <- np$load(paths[min_ix])
    mim <- melt(im) %>%
      filter(value != 0) %>%
      mutate(
        Var1 = xy_grid[i, 1] + (Var1) * imsize / 64,
        Var2 = xy_grid[i, 2] + (Var2) * imsize / 64
      )
    if (nrow(mim) == 0) next
    
    p <- p +
      geom_rect(
        data = mim,
        aes(
          xmin = min(Var1),
          xmax = max(Var1),
          ymin = min(Var2),
          ymax = max(Var2)
        ),
        fill = "#ededed"
      ) +
      geom_tile(
        data = mim,
        aes(x = Var1, y = Var2, fill = as.factor(Var3))
      )
  }
  
  p
}
