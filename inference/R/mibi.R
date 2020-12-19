
load_mibi <- function(data_dir, n_paths = NULL) {
  mibi.sce <- get(load(file.path(data_dir, "mibiSCE.rda")))
  tiff_paths <- list.files(
    file.path(data_dir, "TNBC_shareCellData"),
    "*.tiff",
    full.names = T
  )
  
  if (is.null(n_paths)) {
    n_paths <- length(tiff_paths)
  }
  
  tiff_paths <- tiff_paths[1:n_paths]
  sample_names <- str_extract(tiff_paths, "[0-9]+")
  list(
    tiffs = tiff_paths,
    mibi = mibi.sce[, colData(mibi.sce)$SampleID %in% sample_names]
  )
}

spatial_subsample <- function(tiff_paths, exper, qsize=500) {
  ims <- list()
  for (i in seq_along(tiff_paths)) {
    print(paste0("cropping ", i, "/", length(tiff_paths)))
    r <- raster(tiff_paths[[i]])
    ims[[tiff_paths[[i]]]] <- crop(r, extent(1, qsize, 1, qsize))
  }
  
  cur_cells <- map2_dfr(
    ims, im_id, 
    ~ data.frame(SampleID = .y, cellLabelInImage = unique(as.vector(.x)))
    ) %>%
    unite(sample_by_cell, SampleID, cellLabelInImage, remove = F)
  
  scell <- colData(exper) %>%
    as.data.frame() %>%
    dplyr::select(SampleID, cellLabelInImage) %>%
    unite(sample_by_cell, SampleID, cellLabelInImage) %>%
    .[["sample_by_cell"]]
  
  list(
    ims = ims,
    exper = exper[, scell %in% cur_cells$sample_by_cell]
  )
}

extract_patches <- function(tiff_paths, exper, response = "PD1", qsize = 128) {
  j <- 1
  x <- list()
  y <- list()
  for (i in seq_along(tiff_paths)) {
    r <- raster(tiff_paths[i])
    ix_start <- seq(1, ncol(r), by = qsize)
    r_cells <- matching_cells(tiff_paths[i], exper)
    
    for (w in seq_along(ix_start)) {
      for (h in seq_along(ix_start)) {
        patch <- extract_patch(r, w, h, r_cells)
        x[[j]] <- patch$x
        y[[j]] <- patch$y
        j <- j + 1
      }
    }
  }
  
  list(x = x, y = c(y))
}