def preprocess_cv(path_to_exp, path_to_glucose, path_to_sex):
    X = pd.read_csv(path_to_exp).to_numpy(dtype=float)
    y = pd.read_csv(path_to_glucose).to_numpy(dtype=float)[:,-1]
    sex = pd.read_csv(path_to_sex).to_numpy(dtype=float)
    
    # Cross Validation
    skf_train_test = StratifiedKFold(n_splits=6, shuffle=False)
    indices = [index for index in skf_train_test.split(X,sex)]
    return X, y ,sex, indices
