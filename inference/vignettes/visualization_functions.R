
untar_all <- function(paths, exdir = "archive") {
  for (i in seq_along(paths)) {
    exdir_i <- file.path(exdir, i)
    if (!dir.exists(exdir_i)) {
      untar(paths[i], exdir = exdir_i)
    }
  }
}

align_to_list <- function(Zb, df = F, tol = 0.01) {
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

### Helpers that are useful when a "true" embedding is known

plot_overlay <- function(ud_combined, max_i = 10, level = 0.95, alpha = 0.05) {
  ud_combined <- filter(ud_combined, i < max_i)
  ud_mean <- ud_combined %>%
    group_by(i, y) %>%
    summarise(across(starts_with("X"), mean))
  
  ud_truth <- filter(ud_combined, b == max(b))
  ud_truth_wide <- ud_truth %>%
    rename(X1_true = X1, X2_true = X2) %>%
    left_join(ud_mean %>% select(-i, -y))
  
  ggplot(ud_combined %>% filter(b < max(b)), aes(X1, X2, col = y, fill = y)) +
    stat_ellipse(aes(group = i), geom = "polygon", level = level, type = "norm", alpha = alpha, size = 0.1) +
    geom_point(data = ud_mean, size = 0.8) +
    geom_hline(yintercept = 0, col = "#d3d3d3", size = 0.5) +
    geom_vline(xintercept = 0, col = "#d3d3d3", size = 0.5) +
    scale_color_gradient2(low = "#A6036D", high = "#03178C", mid = "#F7F7F7") +
    scale_fill_gradient2(low = "#A6036D", high = "#03178C", mid = "#F7F7F7") +
    geom_point(data = ud_truth, size = 1, shape = 15) +
    geom_segment(data = ud_truth_wide, aes(xend = X1_true, yend = X2_true), size = 0.3, alpha = 0.8)
}

align_with_truth <- function(ud_hats, U, Sigma, tol = 0.01) {
  c(ud_hats, list(U %*% diag(Sigma))) %>%
    align_to_list(tol = tol, df = T) %>%
    bind_rows(.id = "b") %>%
    group_by(b) %>%
    mutate(i = row_number()) %>%
    ungroup() %>%
    mutate(b = as.integer(b))
}
  
plot_overlay_combined <- function(configuration, means) {
  ggplot(configuration, aes(X1, X2, col = y, fill = y)) +
      stat_ellipse(aes(group = i), geom = "polygon", level = 0.95, type = "norm", alpha = 0.5, size = 0.1) +
      geom_point(data = means, size = 0.1) +
      geom_hline(yintercept = 0, col = "#d3d3d3", size = 0.5) +
      geom_vline(xintercept = 0, col = "#d3d3d3", size = 0.5) +
      scale_color_gradient2(low = "#A6036D", high = "#03178C", mid = "#F7F7F7") +
      scale_fill_gradient2(low = "#A6036D", high = "#03178C", mid = "#F7F7F7") +
      theme(
        axis.text = element_text(size = 8),
        axis.title = element_text(size = 10)
      )
}
