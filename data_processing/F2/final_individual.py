import pandas as pd
from sklearn.model_selection import StratifiedKFold

from sklearn.model_selection import train_test_split

def preprocess_cv(path_to_exp, path_to_glucose, path_to_sex):
    X = pd.read_csv(path_to_exp).to_numpy(dtype=float)[:,1:]
    y = pd.read_csv(path_to_glucose,header=None).to_numpy(dtype=float)

    # Cross Validation
    X_train, X_test, y_train, y_test = train_test_split(
          X, y, test_size=float(1/6), random_state=42)
    print(X.shape, X_test.shape, X_train.shape, y_train.shape,y.shape, y_test.shape)
    return X_train, X_test, y_train, y_test 
