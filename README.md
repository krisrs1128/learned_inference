
These scripts are what's used to run the simulation and data analysis in this
study. They both rely on the functions in the `stability` and `inference` helper
packages, defined at the top of this repository.

## Simulation


## Data Analysis

First, you have to download the raw MIBI-ToF images from [here], along with the
SummarizedExperiment data from
[here](https://drive.google.com/drive/folders/1Qb6VgVkWfy2x5Dr7kzqMAfzOLas1G6v-).
The summarized experiment data gives the expression values and cell categories
for the cells in the original images. We've combined those two sources into a
zipped archive called [`tnbc_raw.tar.gz`]().

To prepare the patches used for training, we have to call the `prepare_mibi.Rmd`
vignette for each of the study participants, `B`,

```
tar -zxvf tnbc_raw.tar.gz
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/prepare_mibi.Rmd', params = list(j = ${B}, data_dir='../../../tnbc_raw/', out_dir='../../../stability_data'))"
mv stability_data/tiles/y.csv stability_data/tiles/y_${B}.csv
tar -zcvf stability_data_${B}.tar.gz stability_data
```

Calling this across different `B`'s creates a different zipped directory for
each patient, each with many patches (in a `tiles/` directory) and measured
responses `y` (log tumor to immune ratio). For the next step, we're going to
split each patient into a train, dev, or test group. This is done using the
`tnbc_splits.ipynb` notebook.

```
for f in $(ls stability_data_*tar.gz); do tar -zxvf $f; done # combines all patients to same directory

cd learned_inference/notebooks/
source learned_inference/.env # used to determine output directory

jupyter nbconvert --to=python tnbc_splits.ipynb
python3 -m tnbc_splits

cd $DATA_DIR
tar -zcvf stability_data.tar.gz stability_data
```

This new version of the `stability_data.tar.gz` archive now has a file called
`Xy.csv` that, in addition to containing raw data about the cell proportions,
has a column `split` ensuring that each patient is fully contained in one of the
train / dev / test splits.

This is the archive that we can use for model training. Before doing anything
complicated, we can run a very simple baseline, using just the pixel counts for
various cell types.

```
cd learned_inference/notebooks/
jupyter nbconvert --to=python tnbc_baseline.ipynb
python3 -m tnbc_baseline
cd ../../
```

To train a single model, we can use the `model_training.ipynb` notebook.

```
tar -zxvf stability_data.tar.gz
cd learned_inference/notebooks/

export TRAIN_YAML = conf/tnbc_cnn.yaml # or whichever model you want it to be
export BOOTSTRAP = 0 # can change for different bootstraps

jupyter nbconvert --to=python model_training.ipynb
python3 -m model_training
```

The saved model and features always go into the `$DATA_DIR` directory, with
relative paths specified `$TRAIN_YAML` file. To make it easy to compare runs
during the stability analysis, we always save the results in the format given by
`$OUTNAME` below,

```
cd $DATA_DIR
rm -rf $DATA_DIR/tiles/ # avoid copying over training data
export OUTNAME=$(basename ${TRAIN_YAML})_${BOOTSTRAP}.tar.gz
tar -zcvf ${OUTNAME} -C $DATA_DIR/ .
```

After running this for many values of `$BOOTSTRAP`, we can visualize the
stability, using the `stability.Rmd` vignette. First, we put all the trained
models into a `stability_outputs` folder, which the script refers to.

```
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/stability.Rmd', params = list(data_dir = '../../../stability_outputs/', layer = 'linear', model_prefix = 'tnbc_cnn', sca = FALSE, save_dir = '../../../figures'))"
```

The parameters here refer to,

* `data_dir`: The directory, relative to the rmarkdown, where all the zipped
  model results are saved.
* `layer`: The layer of model activations to use in the analysis. For the CNN,
  we refer to the `linear` layer just before regression. For the VAE, we refer
  to the mean embedding, `mu`.
* `model_prefix`: The prefix used in the name of the zipped model files. This is
  used so that the final figure names don't overwrite one another from one run
  to another.
* `sca`: Use sparse PCA? Takes longer, but seems to give better results.
* `save_dir`: The directory, relative to the rmarkdown, where all the final
  figures and summary csv's will be saved.

Finally, once this whole process has been run across many different models, you
can visualize some high level summary statistics using the `summary_plots.Rmd`
script.

```
Rscript -e "rmarkdown::render('learned_inference/inference/vignettes/summary_plots.Rmd', params = list(data_dir = '../../../figures/')
```

### On HTCondor

To run many bootstrap versions of a model, it's possible to simply wrap the
commands above in a for loop, but it might take a while -- you would have to
create patches for each patient one at a time, and would run the (totally
independent) models sequentially. We instead run them in parallel, using
`HTCondor`'s queueing functionality. (`HTCondor` is also how we have access to
GPU resources). At the end of the day, all the commands above can be summarized
in the condor jobs in the `run_scripts` directory,

```
# create training data
condor_submit patch.submit
for f in $(ls stability_data_*tar.gz); do tar -zxvf $f; done
tar -zcvf stability_data.tar.gz stability_data/

# define train / test splits and train
condor_submit tnbc_splits.submit
bash train.submit conf/train_cnn.yaml # or whichever model to run

# visualize
mv tnbc_cnn*tar.gz stability_outputs/
tar -zcvf stability_outputs.tar.gz stability_outputs/
condor_submit visualize_outputs.submit
```

You have to wait until each job is finished before launching the next. The
longest step (training) takes about 25 minutes per model, though their start
times might be staggered.
