#!/usr/bin/env python
import sklearn.linear_model as lm
import torch

def train_elnet(model, loader, **kwargs)::
    D, y = random_features(model, loader)
    elnet_model = lm.Elnet(**kwargs)
    elnet_model.fit(X = D, y = y)
    y_hat = elnet_model.predict(X = D)
    return elnet_model, D, y_hat


def random_features(model, loader, device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    D, y = [], []
    for x, _ in loader:
        x = x.to(device)
        with torch.no_grad():
            D.append(model(x).cpu())
            y.append(y)

    D = torch.cat(D).squeeze()
    y = torch.cat(y).squeeze()
    return D, y


def predict_rcf(model, elnet_model, loader):
    D, y = random_features(model, loader)
    y_hat = elnet_model.predict(X = D)
    return D, y_hat, y


def train_rcf(elnet_model, opts, out_paths, writer):
    metadata, errors = [], {}
    for split in ["dev", "test"]:
        _, y_hat, y = predict_rcf(model, elnet_model, loaders[split])
        errors[split] = np.mean((y - y_hat) ** 2)
        np.save(out_paths[0] / f"{split}_features.csv", D)

    D = random_features(loaders["features"])
