
source .env
source ~/.virtualenvs/learned_inference/activate
cd $ROOT_DIR/inference/
Rscript -e "rmarkdown::render('vignettes/generate.Rmd')"
cd $ROOT_DIR/learning/
python3 -m data
python3 -m bootstrap -c ../conf/train.yaml
python3 -m train -c ../conf/train.yaml
python3 -m features -c ../conf/train.yaml -m $DATA_DIR/runs/vae_20200711/model_40.pt