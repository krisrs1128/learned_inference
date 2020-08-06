"""
Helpers to Generate Config Files
"""
from addict import Dict
import pathlib
import yaml

def fine_tune_yaml(original_yaml, out_dir, start_epoch=0):
    conf = yaml.safe_load(open(original_yaml, "r"))
    conf["organization"]["out_dir"] = str(pathlib.Path("runs", f"vae_tune_{start_epoch}"))
    conf["organization"]["features_dir"] = str(pathlib.Path("features", f"vae_tune_{start_epoch}"))
    conf["train"]["checkpoint"] = str(pathlib.Path("runs", "vae_no_boot", "None", f"model_{start_epoch}.pt"))
    conf["train"]["n_epochs"] = conf["train"]["n_epochs"] - start_epoch - 1

    with open(pathlib.Path(out_dir, f"start_{start_epoch}.yaml"), "w") as f:
        yaml.dump(conf, f, default_flow_style=False)


def fine_tune_sh(out_dir, start_epoch):
    lines = ["#!/bin/bash",
             "tar -zxvf $_CONDOR_SCRATCH_DIR/data.tar.gz",
             "cd /home/kris/",
             "source .env",
             "cd learning",
             f"python3 -m bootstrap -c ../conf/fine_tuning/start_{start_epoch}.yaml",
             f"python3 -m train -c ../conf/fine_tuning/start_{start_epoch}.yaml -b ${{1}}",
             "cd $_CONDOR_SCRATCH_DIR/",
             "python3 -m features -c ../conf/start_{start_epoch}.yaml -m $DATA_DIR/features/",
             "tar -zcvf data_output_${2}_${1}.tar.gz $DATA_DIR/features/"]

    with open(pathlib.Path(out_dir, f"train_{start_epoch}.sh"), "w") as f:
        f.write('\n'.join(lines))

def coreset_yaml():
    pass

def coreset_sh():
    pass


if __name__ == '__main__':
        for epoch in range(0, 60, 10):
            fine_tune_yaml("../conf/train_boot.yaml", "../conf/fine_tuning/", epoch)
            fine_tune_sh("../run_scripts/fine_tuning", epoch)
