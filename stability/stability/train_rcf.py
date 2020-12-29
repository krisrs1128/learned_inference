#!/usr/bin/env python
import sklearn.linear_model as lm
import torch

def train_elnet(model, loader, **kwargs)::
    D, y = random_features(model, loader)
    elnet_model = lm.Elnet(**kwargs)
    elnet_model.fit(X = D, y = y)
    y_hat = elnet_model.predict(X = D)
    return elnet_model, (D, y), y_hat


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


def train_rcf(model, loader, opts, out_paths, writer):
    metadata, errors = [], {}

    elnet_model, Dy, y_hat = train_elnet(model, loader)
    toch.save(model.state_dict(), f"patches-{out_paths[2]}")
    np.save(f"sk-{(out_paths[2]).replace('pt', '')}.npy", elnet_model.coef_)

    # get errors
    errors["train"] = np.mean((Dy[1] - y_hat) ** 2)
    for split in ["dev", "test"]:
        _, y_hat, y = predict_rcf(model, elnet_model, loaders[split])
        errors[split] = np.mean((y - y_hat) ** 2)
    json.dumps(errors, open(out_paths[0] / "logs", "errors.json", "w"))

    # save full feature set
    D = random_features(loaders["features"])
    k_path = Path(out_paths[0]) / "full_best.npy"
    np.save(out_paths, k_path)
    metadata.append({"epoch": "best", "layer": "full", "out_path": k_path})

    # save features reweighted by coefficient

    # save metadata
    metadata = pd.DataFrame(metadata)
    metadata.to_csv(out_paths[1])
