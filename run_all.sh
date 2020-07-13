
Rscript -e "rmarkdown::render('sim/generate.Rmd')"
source venv/bin/activate
python3 -m sim.data
python3 -m sim.vae -c conf/train.yaml
python3 -m sim.features -c conf/train.yaml -m data/runs/vae_20200711/model_140.pt
