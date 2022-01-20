
To generate outputs from three bootstrap strategies, we can use the
`bootstrap_vis_*.Rmd` notebooks. Those can then be studied in downstream
visualization scripts.

The block below computes the bootstrap outputs for all the simulation
configurations,

```
for s in 15 50 90; do
  for k in 32 64 128; do
    for script in parametric nonparametric compromise; do
      echo $s $k $script;
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='cnn-k${k}-${s}', layer_prefix='linear_best*', transform='log'))"
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='vae-k${k}-${s}', layer_prefix='mu_best*'))"
    done;
  done;
done;
```

The analogous run for the data analysis visualizations is given below,
