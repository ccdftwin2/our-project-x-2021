import pandas as pd
from sklearn.model_selection import StratifiedKFold

def preprocess_cv(path_to_exp, path_to_glucose, path_to_sex):
    X = pd.read_csv(path_to_exp).to_numpy(dtype=float)[:,1:]
    y = pd.read_csv(path_to_glucose,header=None).to_numpy(dtype=float)
    sex = pd.read_csv(path_to_sex,header=None).to_numpy(dtype=float)
    print(y.shape, sex.shape,X.shape)
    # Cross Validation
    skf_train_test = StratifiedKFold(n_splits=6, shuffle=False)
    indices = [index for index in skf_train_test.split(X,sex)]
    return X, y ,sex, indices
