
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
    .[["sample_by_cell"]]
  
  list(
    ims = ims,
    exper = exper[, scell %in% cur_cells$sample_by_cell]
  )
}

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

extract_patch <- function(r, w, h, r_cells, response, qsize = 128) {
  r <- crop(r, extent(w, w + qsize, h, h + qsize))
  cur_cells <- colData(exper)$cellLabelInImage %in% unique(as.vector(r))
  y <- mean(assay(exper)[response, cur_cells] > 0) # proportion of active cells
  
  list(x = r, y = y)
}

extract_patches <- function(tiff_paths, exper, response = "PD1", qsize = 128, 
                            out_dir = ".") {
  im_ids <- str_extract(tiff_paths, "[0-9]+")
  y_path <- file.path(out_dir, "y.csv")
  
  j <- 1
  for (i in seq_along(tiff_paths)) {
    print(i)
    r <- raster(tiff_paths[i])
    ix_start <- seq(1, ncol(r), by = qsize)
    print(ix_start)
    r_cells <- subset_exper(im_ids[i], r, exper)
    
    for (w in seq_along(ix_start)) {
      for (h in seq_along(ix_start)) {
        patch <- extract_patch(r, ix_start[w], ix_start[h], r_cells, response, qsize)
        
        # write results
        raster_path <- file.path(out_dir, sprintf("patch_%s_%s-%s.tiff", i, w, h))
        writeRaster(patch$x, file.path(raster_path), format="GTiff", overwrite=TRUE)
        y <- data.frame(path = tiff_paths[i], i = i, w = w, h = h, y = patch$y)       
        write.table(y, y_path, sep = ",", col.names = !file.exists(y_path), append = T)
        
        j <- j + 1
      }
    }
  }
  
}