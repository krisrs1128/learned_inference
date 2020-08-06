
source ../.env
source ~/.virtualenvs/learned_inference/bin/activate
cd $ROOT_DIR/inference/
Rscript -e "rmarkdown::render('vignettes/generate.Rmd')"
cd $ROOT_DIR/learning/
python3 -m data

bash cluster.submit ../conf/fine_tuning/start_10.yaml

python3 -m train -c ../conf/train_no_boot.yaml
python3 -m features -c ../conf/train_no_boot.yaml -m $DATA_DIR/runs/vae_no_boot/

python3 -m bootstrap -c ../conf/train.yaml
python3 -m train -c ../conf/train_boot.yaml -b 1
python3 -m train -c ../conf/train_boot.yaml -b 2
python3 -m train -c ../conf/train_boot.yaml -b 10

python3 -m features -c ../conf/fine_tuning/start_50.yaml -m $DATA_DIR/data/runs/fine_tuning -e 20
python3 -m features -c ../conf/fine_tuning/start_10.yaml -m $DATA_DIR/runs/fine_tuning -e 60

Rscript -e "rmarkdown::render('vignettes/coresets.Rmd', params=list(space=250))"
Rscript -e "rmarkdown::render('vignettes/coresets.Rmd', params=list(space=500))"
Rscript -e "rmarkdown::render('vignettes/coresets.Rmd', params=list(space=1000))"
Rscript -e "rmarkdown::render('vignettes/coresets.Rmd', params=list(space=2000))"
python3 -m train -c ../conf/train_coreset.yaml
