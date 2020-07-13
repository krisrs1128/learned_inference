
source .env
source venv/bin/activate
Rscript -e "rmarkdown::render('sim/generate.Rmd')"
python3 -m sim.data
python3 -m sim.vae -c conf/train.yaml
python3 -m sim.features -c conf/train.yaml -m data/runs/vae_20200711/model_90.pt
