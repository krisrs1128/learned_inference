
To run all the simulation experiments, you can use the loop below.

```
for model in cnn vae; do
  for k in 32 64 128; do
    for s in 15 50 90; do
      echo $k $s;
      bash train.submit conf/${model}-k${k}-${s}.yaml stability_data_sim.tar.gz
    done;
  done;
done;
```
