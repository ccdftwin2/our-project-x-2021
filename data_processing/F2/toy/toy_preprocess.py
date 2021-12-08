import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold

def toy_preprocess(hypo_int2_final, F2_BTBR_clinic):
    # Load the data
    dfx = pd.read_csv (hypo_int2_final,index_col=False)
    dfx['Unnamed: 0'] = [x[-4:] for x in dfx['Unnamed: 0']]
    dfx.head()

    # Load the clinical traits
    dfy = pd.read_csv (F2_BTBR_clinic)
    dfy.head()

    # Now we process the data
    #
    
    # Now match the mouse index between the clincic traits and gene expression data
    # Notice that the glucose data for F2 at 10 week is "Unnamed: 25" ,
    # sex is "Unamed: 1",
    # and mouse id is "Unnamed: 0" as above
    #
    X = dfx.to_numpy(dtype=float) # Expression level: (num of mice, num of genes)
    y = []                  # Glucose level: (num of mice, its glucose level from 4 wk - 10 wk)
    sex = []                # Sex for each mice, 0 for male, 1 for female

    for id in dfx['Unnamed: 0']:
        i = dfy.index[dfy['Unnamed: 0'] == id].tolist()
        if len(i)!= 0:
            i = i[0]
            y.append([dfy["Unnamed: 7"][i],dfy["Unnamed: 13"][i],dfy["Unnamed: 19"][i],dfy["Unnamed: 25"][i]])
            sex.append(0 if dfy["Unnamed: 1"][i] == "M" else 1)

    sex = np.array(sex,dtype=int)
    y = np.array(y,dtype=float)
    y.shape,sex.shape,X.shape

    # X may contains NaN value, replace it with 0
    for i in range(len(X)):
        for j in range(len(X[0])):
            if np.isnan(X[i][j]):
                X[i][j] = 0.0

    X = np.array(X,dtype=float)

    # Cross Validation
    indices = [] # CV indices

    skf_train_test = StratifiedKFold(n_splits=6, shuffle=False)
    for index1 in skf_train_test.split(X,sex):
        X_temp = [X[i] for i in index1[0]]
        sex_temp = [sex[i] for i in index1[0]]
        skf_train_val = StratifiedKFold(n_splits=5, shuffle=False)
        for index2 in skf_train_val.split(X_temp,sex_temp):
            tvt = list(index2)
            tvt.append(index1[1])
            indices.append(tvt) # Represent (train:test:val)

    print(len(indices)," Combinations, Train: ",len(indices[1][0])," Test: ", len(indices[1][1])," Val: ",len(indices[1][2]))

    # Split the train, test, validation datasets
    X_train = np.array([X[i] for i in indices[0][0]])
    sex_train = np.array([sex[i] for i in indices[0][0]])
    y_train = np.array([y[i] for i in indices[0][0]])[:,-1]

    X_val = np.array([X[i] for i in indices[0][1]])
    sex_val = np.array([sex[i] for i in indices[0][1]])
    y_val = np.array([y[i] for i in indices[0][1]])[:,-1]

    X_test = np.array([X[i] for i in indices[0][2]])
    sex_test = np.array([sex[i] for i in indices[0][2]])
    y_test = np.array([y[i] for i in indices[0][2]])[:,-1]

    return X_train, sex_train, y_train, X_val, sex_val, y_val, X_test, sex_test, y_test

def five_tissues_preprocess(path_to_combined, path_to_glucose, path_to_sex):

    df_adi = pd.read_csv(path_to_combined, index_col = False, header=None)
    df_adi_gluc = pd.read_csv(path_to_glucose, header=None)
    df_adi_sex = pd.read_csv(path_to_sex, header=None)
    
    X = np.array(df_adi, dtype="float")
    y = np.array(df_adi_gluc, dtype="float")
    y = y[~np.isnan(X).any(axis=1)]
    sex = np.array(df_adi_sex)
    sex = sex[~np.isnan(X).any(axis=1)]
    X = X[~np.isnan(X).any(axis=1)]
    
    # Cross Validation
    indices = [] # CV indice
    skf_train_test = StratifiedKFold(n_splits=6, shuffle=False)
    for index1 in skf_train_test.split(X,sex):
        X_temp = [X[i] for i in index1[0]]
        sex_temp = [sex[i] for i in index1[0]]
        skf_train_val = StratifiedKFold(n_splits=5, shuffle=False)
        for index2 in skf_train_val.split(X_temp,sex_temp):
            tvt = list(index2)
            tvt.append(index1[1])
            indices.append(tvt) # Represent (train:test:val)
            
    #print(len(indices)," Combinations, Train: ",len(indices[1][0])," Test: ", len(indices[1][1])," Val: ",len(indices[1][2])
    
    # Split the train, test, validation datasets
    X_train = np.array([X[i] for i in indices[0][0]])
    sex_train = np.array([sex[i] for i in indices[0][0]])
    y_train = np.array([y[i] for i in indices[0][0]])
    
    X_val = np.array([X[i] for i in indices[0][1]])
    sex_val = np.array([sex[i] for i in indices[0][1]])
    y_val = np.array([y[i] for i in indices[0][1]])
    
    X_test = np.array([X[i] for i in indices[0][2]])
    sex_test = np.array([sex[i] for i in indices[0][2]])
    y_test = np.array([y[i] for i in indices[0][2]])

    return X_train, sex_train, y_train, X_val, sex_val, y_val, X_test, sex_test, y_test
    
