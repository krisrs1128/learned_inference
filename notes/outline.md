
I. Premise
  A. we can now describe samples using data types that are not the standard
  substrates for statistical analysis
    1. We'll focus on: mibi in single cell and satellite in public health
    2. We want to draw reproducible conclusions about features that are in
    these data, and how they are associated with outcomes of interest
      a. E.g., cancer survival or public health effectiveness
  B. Natural enough idea is to apply sophisticated feature learning, followed
  by high-dimensional inference
    1. We'll compare a few different ways of implementing this research program
    2. prediction: We'll look at how much better prediction is compared to
    non-image features, and we'll also see how much worse it is than learning
    end to end
    3. selection: We'll examine the stability of the inferences that you draw
II. Contributions
  A. Feature learning analogy: pca and supervised pca
    1. We'll see whether the analogy of "valid features" when not looking at Y
    continues (it really should)
    2. We'll see what the power and sparsity tradeoffs look like, when you go
    from learning X-features using whole dataset to learning XY features using
    only half
  B. We'll give a few practical approaches to deriving / aggregating features
  from images (known in ML, but not really statistics), and examine their
  appropriateness
    1. Autoencoders
      a. For satellites and mibi, gives representation at granular level. Then,
         compare the density of cells / neighborhoods in different parts of
         autoencoder space, and use them as predictors in addition to the usual
         cell / neighborhood features.
    2. tile2vec
      a. Same idea as autoencoders, but supposedly more suited towards mapping
    3. CNNs
      a. Analogy is supervised pca / partial least squares
      b. We can't learn features on the same sets we use to do inference
    4. Graphs
      a. For single-cell, this is how cell types are linked to one another
      b. For satellites, this is how different land types relate?
  C. We'll examine how inference and interpretation works in this setting
    1. The main difference is that the features we learn may not be stable from
    one investigation to another.
      a. We'll check out whether we can at least correlate the feature subspaces
      with one another
      b. We'll see how the correlation between features really affects things
    2. We'll also compare with a "two-step" procedure that regresses onto the
    residuals from the non-image features
  D. We'll release all our beautiful code and singularity images
  E. We may not be inventing anything that novel here, but we will share some
     things we learned that no one in the world knows
III. Methodology
IV. Simulation Experiments
  A. 
V. Data Analysis
  A. Spatial Single-Cell
    1. Show survival prediction performance
      a. with and without the cell-level features, from different feature
      extraction procedures
    2. Show the inferred spatial features
      a. Give visualization for significant ones: images that have high and low
      scores
    3. Show the alignment between learned features
  B. Sensed Public Health
    1. Show ___ prediction performance
    2. Show the inferred spatial features
    3. Show alignment between features
VI. Discussion
  A. We need to think of both feature learning and inference, for many real
  modern biostatistical (molecular or public health) problems
  B. Less of our data will be tabular sensed measurements
    1. Much more raw data -- sensor streams, images, audio
    2. Deep learning has been successful with using these raw streams for better
       prediction
    3. But we haven't learned how to use those streams to draw better
       generalizable inferences in more sensitive contexts
