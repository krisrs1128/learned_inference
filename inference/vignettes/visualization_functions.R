
untar_all <- function(paths) {
  for (i in seq_along(paths)) {
    exdir <- file.path(str_replace(paths[[i]], ".tar.gz", ""))
    if (!dir.exists(exdir)) {
      untar(paths[i], exdir = exdir)
    }
  }
}

align_to_list <- function(Zb, df = F, tol = 0.001) {
  procrustes(Zb, tol = tol) %>%
    .[["x_align"]] %>%
    arr_to_list(df = df)
}

plot_facets <- function(ud_combined, max_i = 10, level = 0.9, facet = TRUE, alpha = 0.05) {
  ud_combined <- filter(ud_combined, i < max_i)
  ud_mean <- ud_combined %>%
    group_by(i, y) %>%
    summarise(across(starts_with("X"), mean))
  
  p <- ggplot(ud_combined, aes(X1, X2, col = y, fill = y)) +
    stat_ellipse(aes(group = i), geom = "polygon", level = level, type = "norm", alpha = alpha, size = 0.1) +
    geom_point(data = ud_mean, size = 0.8) +
    geom_hline(yintercept = 0, col = "#d3d3d3", size = 0.5) +
    geom_vline(xintercept = 0, col = "#d3d3d3", size = 0.5) +
    scale_color_gradient2(low = "#A6036D", high = "#03178C", mid = "#F7F7F7") +
    scale_fill_gradient2(low = "#A6036D", high = "#03178C", mid = "#F7F7F7") +
    theme(
      axis.text = element_text(size = 8),
      axis.title = element_text(size = 10)
    )
  if (facet) {
    p <- p + facet_wrap(~ i, scale = "free")
  }
  p
}