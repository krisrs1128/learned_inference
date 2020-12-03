#!/usr/bin/env bash
condor_submit cluster.submit conf/vae15.yaml
condor_submit cluster.submit conf/vae50.yaml
condor_submit cluster.submit conf/vae90.yaml
condor_submit cluster.submit conf/cnn15.yaml
condor_submit cluster.submit conf/cnn50.yaml
condor_submit cluster.submit conf/cnn90.yaml
