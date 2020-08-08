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
    conf["train"]["n_epochs"] = max(conf["train"]["n_epochs"] - start_epoch - 1, 1)

    pathlib.Path(out_dir).mkdir(exist_ok=True)
    with open(pathlib.Path(out_dir, f"start_{start_epoch}.yaml"), "w") as f:
        yaml.dump(conf, f, default_flow_style=False)


def coreset_yaml(original_yaml, out_dir, size=100, n_epochs=400):
    conf = yaml.safe_load(open(original_yaml, "r"))
    conf["organization"]["out_dir"] = str(pathlib.Path("runs", f"vae_coreset_{size}"))
    conf["organization"]["features_dir"] = str(pathlib.Path("features", f"vae_coreset_{size}"))
    conf["train"]["checkpoint"] = str(pathlib.Path("runs", "vae_no_boot", "None", f"model_final.pt"))
    conf["train"]["n_epochs"] = n_epochs

    pathlib.Path(out_dir).mkdir(exist_ok=True)
    with open(pathlib.Path(out_dir, f"coreset_{size}.yaml"), "w") as f:
        yaml.dump(conf, f, default_flow_style=False)


def cluster_submit(out_dir, conf_path="train", output_name="cluster.submit", B=50):
    lines = ["#!/bin/bash",
             "universe = docker",
             "log = /home/ksankaran/logs/job_$(Cluster).log",
             "error = /home/ksankaran/logs/job_$(Cluster)_$(Process).err",
             "output = /home/ksankaran/logs/job_$(Cluster)_$(Process).out",
             "docker_image = krisrs1128/learned_inference_d2",
             "input = data.tar.gz",
             "transfer_output_files = data_output_$(Cluster)_$(Process).tar.gz",
             "executable = train.sh",
             f"arguments = \"'{conf_path}' $(Process) $(Cluster)\"",
             # "request_gpus = 1",
             # "+WantGPULab = true",
             # '+GPUJobLength = "short"',
             "request_cpus = 1",
             "request_memory = 4GB",
             "request_disk = 1GB",
             f"queue {B}"]

    with open(pathlib.Path(out_dir, output_name), "w") as f:
        f.write('\n'.join(lines))


if __name__ == '__main__':
        for epoch in range(0, 70, 10):
            fine_tune_yaml("../conf/train_boot.yaml", "../conf/fine_tuning/", epoch)
            cluster_submit("../run_scripts/", f"../conf/fine_tuning/start_{epoch}.yaml", f"tune_{epoch}.submit")

        for size in [250, 500, 1000, 2000]:
            coreset_yaml("../conf/train_boot.yaml", "../conf/coreset/", size)
            cluster_submit("../run_scripts/", f"../conf/coreset/coreset_{size}.yaml", f"cluster_{size}.submit")
