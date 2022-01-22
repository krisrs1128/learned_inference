
To generate outputs from three bootstrap strategies, we can use the
`bootstrap_vis_*.Rmd` notebooks. Those can then be studied in downstream
visualization scripts.

The block below computes the bootstrap outputs for all the simulation
configurations,

```
for s in 15 50 90; do
  for script in parametric nonparametric compromise; do
    for k in 32 64 128; do
      echo $s $k $script;
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='cnn-k${k}-${s}', layer_prefix='linear_best*', transform='log'))"
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='vae-k${k}-${s}', layer_prefix='mu_best*'))"
    done;

    for k in 256 512 1024; do
      echo $s $k $script;
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='rcf-k${k}-${s}', layer_prefix='full_best*'))"
    done;
  done;
done;

export k=64
export s=90
for script in parametric nonparametric compromise; do
  Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='vae-k${k}-${s}', layer_prefix='mu_best*'))"
done
```

The analogous run for the data analysis visualizations is given below,

```
for s in 15 50 90; do
  for script in parametric nonparametric compromise; do
    for k in 32 64 128; do
      echo $s $k $script;
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='tnbc_cnn-k${k}', layer_prefix='linear_best*', transform='log', input_dir = 'data/data_analysis_outputs/'))"
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='tnbc_vae-k${k}', layer_prefix='mu_best*', input_dir = 'data/data_analysis_outputs/'))"
    done;

    for k in 256 512 1024; do
      echo $s $k $script;
      Rscript -e "rmarkdown::render('bootstrap_vis_${script}.Rmd', params = list(subset='tnbc_rcf-k${k}', layer_prefix='full_best*', input_dir = 'data/data_analysis_outputs/'))"
    done;
  done;
done;
```
