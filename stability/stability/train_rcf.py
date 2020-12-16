
def train_rcf(model, loader, opts, out_paths, writer):
    D, y = random_features(model, loader)
    ridge_model = lm.Ridge()
    ridge_model.fit(X = D, y = y)
    y_hat = ridge_model.predict(X = D)
    return ridge_model, D, y_hat

def random_features(model, loader, device=None):
    if device is None:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    D = []
    y = []
    for x, _ in loader:
        x = x.to(device)
        with torch.no_grad():
            D.append(model(x).cpu())
            y.append(y)

    D = torch.cat(D).squeeze()
    y = torch.cat(y).squeeze()
    return D, y

def predict_rcf(model, ridge_model, loader):
    D, y = random_features(model, loader)
    y_hat = ridge_model.predict(X = D)
    return D, y_hat, y
