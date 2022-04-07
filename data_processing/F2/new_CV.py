import pandas as pd
from sklearn.model_selection import StratifiedKFold
import random

def preprocess_cv(path_to_exp, path_to_glucose, path_to_sex):

    # load dataset
    X = pd.read_csv(path_to_exp).to_numpy(dtype=float)[:,1:]
    y = pd.read_csv(path_to_glucose,header=None).to_numpy(dtype=float)
    sex = pd.read_csv(path_to_sex,header=None).to_numpy(dtype=float)
    print(y.shape, sex.shape,X.shape)
    
    ## Cross Validation
    random.seed(2022)
    indices = [] # CV indices: each element represents one CV set as [training indices, testing indices]
    skf_train_test = StratifiedKFold(n_splits=10, shuffle=False)
    indices_cv,indices_final_test = next(skf_train_test.split(X,sex))
    
    # generate data for final testing, that should not be touched when training
    X_final_test = [X[i] for i in indices_final_test]
    sex_final_test = [sex[i] for i in indices_final_test]
    y_final_test = [y[i] for i in indices_final_test]
    
    # Cross Validation set for training process
    skf_train_val = StratifiedKFold(n_splits=9, shuffle=False)
    X_train = [X[i] for i in indices_cv]
    sex_train = [sex[i] for i in indices_cv]
    y_train = [y[i] for i in indices_cv]
    
    for idx in skf_train_val.split(X_train,sex_train):
        indices.append(idx)
    
    # return: final testing dataset
    #         training dataset with its CV indices 
    return X_train,y_train,indices,X_final_test,y_final_test,
    