
#' @importFrom SummarizedExperiment colData
#' @importFrom forcats fct_lump_n
#' @importFrom stringr str_extract
#' @export
load_mibi <- function(data_dir, n_paths = NULL, n_lev=6) {
  exper <- get(load(file.path(data_dir, "mibiSCE.rda")))
  tiff_paths <- list.files(
    file.path(data_dir, "TNBC_shareCellData"),
    "*.tiff",
    full.names = T
  )

  if (is.null(n_paths)) {
    n_paths <- length(tiff_paths)
  }

  # create a cell-type column
  colData(exper)$cell_type <- colData(exper)$tumor_group
  immune_ix <- colData(exper)$cell_type == "Immune"
  colData(exper)$cell_type[immune_ix] <- colData(exper)$immune_group[immune_ix]
  colData(exper)$cell_type <- fct_lump_n(colData(exper)$cell_type, n_lev)

  # subset to those samples with images
  tiff_paths <- tiff_paths[1:n_paths]
  sample_names <- str_extract(tiff_paths, "[0-9]+")
  list(
    tiffs = tiff_paths,
    mibi = exper[, colData(exper)$SampleID %in% sample_names],
    levels = table(colData(exper)$cell_type)
  )
}

#' @importFrom stringr str_extract
#' @importFrom raster crop raster
#' @importFrom purrr map2_dfr
#' @importFrom tidyr unite
#' @importFrom dplyr select pull
#' @importFrom SummarizedExperiment colData
#' @export
spatial_subsample <- function(tiff_paths, exper, qsize=500) {
  ims <- list()
  for (i in seq_along(tiff_paths)) {
    print(paste0("cropping ", i, "/", length(tiff_paths)))
    r <- raster(tiff_paths[[i]])
    ims[[tiff_paths[[i]]]] <- crop(r, extent(1, qsize, 1, qsize))
  }

  im_ids <- str_extract(tiff_paths, "[0-9]+")
  cur_cells <- map2_dfr(
    ims, im_ids,
    ~ data.frame(SampleID = .y, cellLabelInImage = unique(as.vector(.x)))
    ) %>%
    unite(sample_by_cell, SampleID, cellLabelInImage, remove = F)

  scell <- colData(exper) %>%
    as.data.frame() %>%
    dplyr::select(SampleID, cellLabelInImage) %>%
    unite(sample_by_cell, SampleID, cellLabelInImage) %>%
    pull("sample_by_cell")

  list(
    ims = ims,
    exper = exper[, scell %in% cur_cells$sample_by_cell]
  )
}

#' @importFrom dplyr select pull
#' @importFrom tidyr unite
#' @importFrom SummarizedExperiment colData
#' @export
subset_exper <- function(id, r, exper) {
  scell <- colData(exper) %>%
    as.data.frame() %>%
    dplyr::select(SampleID, cellLabelInImage) %>%
    unite(sample_by_cell, SampleID, cellLabelInImage) %>%
    pull("sample_by_cell")

  sample_by_cell <- data.frame(
    SampleID = id,
    cellLabelInImage = unique(as.vector(r))
  ) %>%
  unite(sample_by_cell, SampleID, cellLabelInImage, remove = F)

  exper[, scell %in% sample_by_cell$sample_by_cell]
}

#' @importFrom dplyr filter pull
#' @importFrom SummarizedExperiment colData
unwrap_channels <- function(r, r_cells) {
  cell_types <- levels(r_cells$cell_type)
  r_mat <- array(0, dim = c(dim(r)[1:2], length(cell_types)))
  for (i in seq_along(cell_types)) {
    cur_cells <- colData(r_cells) %>%
      as.data.frame() %>%
      filter(cell_type == cell_types[i]) %>%
      pull(cellLabelInImage) %>%
      unique()

    r_mat[,, i] <- 1 * as.matrix(r %in% cur_cells)
  }
  r_mat
}

#' @importFrom raster extent crop
#' @importFrom SummarizedExperiment colData assay
extract_patch <- function(r, w, h, r_cells, response, qsize = 256, fct = 4) {
  r <- crop(r, extent(w, w + qsize, h, h + qsize))
  cur_cells <- colData(exper)$cellLabelInImage %in% unique(as.vector(r))
  r <- aggregate(r, fct)
  r <- unwrap_channels(r, r_cells)

  y <- mean(assay(exper)[response, cur_cells] > 0) # proportion of active cells
  list(x = r, y = y)
}

#' @importFrom raster raster extent crop
#' @importFrom SummarizedExperiment colData
#' @importFrom reticulate import
#' @importFrom stringr str_extract
#' @export
extract_patches <- function(tiff_paths, exper, response = "PD1", qsize = 256,
                            out_dir = ".") {
  np <- reticulate::import("numpy")
  im_ids <- str_extract(tiff_paths, "[0-9]+")
  print(im_ids)
  y_path <- file.path(out_dir, "y.csv")

  for (i in seq_along(tiff_paths)) {
    print(i)
    r <- raster(tiff_paths[i])
    ix_start <- seq(0, ncol(r) - qsize/2 - 1, by = qsize/2)
    print(ix_start)
    r_cells <- subset_exper(im_ids[i], r, exper)

    for (w in seq_along(ix_start)) {
      for (h in seq_along(ix_start)) {
        patch <- extract_patch(r, ix_start[w], ix_start[h], r_cells, response, qsize)

        # write results
        npy_path <- file.path(out_dir, sprintf("patch_%s_%s-%s.npy", i, w, h))
        np$save(npy_path, patch$x)
        y <- data.frame(path = tiff_paths[i], i = i, w = w, h = h, y = patch$y)
        write.table(y, y_path, sep = ",", col.names = !file.exists(y_path), append = T)
      }
    }
  }

}