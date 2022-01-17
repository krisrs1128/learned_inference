
To run all the simulation experiments, you can use the loop below.

```
for s in 15 50 90; do

  # vae and cnn models
  for k in 32 64 128; do
    for model in cnn vae; do
      bash train.submit conf/${model}-k${k}-${s}.yaml stability_data_sim.tar.gz
    done;
  done;

  # rcf model
  for k in 256 512 1024; do
    bash train.submit conf/rcf-k${k}-${s}.yaml stability_data_sim.tar.gz
  done;
done;
```

To run the different models for data analysis, we can use

```
for k in 32 64 128; do
  for model in cnn vae; do
    bash train.submit conf/tnbc_${model}-k${k}.yaml stability_data_tnbc.tar.gz
  done;
done;

for k in 256 512 1024; do
  bash train.submit conf/tnbc_rcf-k${k}.yaml stability_data_tnbc.tar.gz
done;
```
