#!/usr/bin/env bash
bash cluster.submit conf/vae15.yaml
bash cluster.submit conf/vae50.yaml
bash cluster.submit conf/vae90.yaml
bash cluster.submit conf/cnn15.yaml
bash cluster.submit conf/cnn50.yaml
bash cluster.submit conf/cnn90.yaml
bash cluster.submit conf/rcf15.yaml
bash cluster.submit conf/rcf50.yaml
bash cluster.submit conf/rcf90.yaml
