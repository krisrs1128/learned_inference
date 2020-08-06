
source ../.env
source ~/.virtualenvs/learned_inference/bin/activate
cd $ROOT_DIR/inference/
Rscript -e "rmarkdown::render('vignettes/generate.Rmd')"
cd $ROOT_DIR/learning/
python3 -m data
python3 -m train -c ../conf/train_no_boot.yaml
python3 -m bootstrap -c ../conf/train.yaml
python3 -m train -c ../conf/train.yaml -b 19
python3 -m features -c ../conf/train_no_boot.yaml -m $DATA_DIR/runs/vae_no_boot/
python3 -m features -c ../conf/fine_tuning/start_50.yaml -m $DATA_DIR/data/runs/fine_tuning -e 20
python3 -m features -c ../conf/fine_tuning/start_10.yaml -m $DATA_DIR/runs/fine_tuning -e 60
python3 -m train -c ../conf/train_coreset.yaml
