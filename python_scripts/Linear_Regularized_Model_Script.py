# Import all the libraries we need.
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
import tensorflow as tf
import tensorflow_probability as tfp
import datetime
import os
from scipy.stats import spearmanr

# Variable for the current directory
cwd = os.getcwd()

#################### IMPORT THE FUNCTIONS WE NEED FROM MODEL AND EVALUATION TODO ####################
#os.chdir("**Put here the directory where you have the file with your function**")
#from file import function

#os.chdir("**Put here the directory where you have the file with your function**")
#from file2 import function2, function3

# For the toy dataprocessing
os.chdir(cwd + '/../data_processing/F2/toy/')
from toy_preprocess import toy_preprocess

# For the toy model script
os.chdir(cwd + '/../models/')
from Linear_Regularized_Model import toy_model

# For the toy evaluations scripts
os.chdir(cwd + '/../evaluations/toy_eval/')
from toy_eval import pearson_corr, spearman_rankcor

# Change back to the current working directory
os.chdir(cwd)
#########################################################################################################

########### TODO: Read in the arguments from the CHTC script. ###########################################
# This will be important for hyperparameter tuning. No arguments for toy script.

# TODO: Run the preprocessing script to get the dataset
# The data paths will be IN THE CURRENT WORKING DIRECTORY (see toy.sh)
# Will have lots of outputs if using cross-validation
X_train, sex_train, y_train, X_val, sex_val, y_val, X_test, sex_test, y_test \
    = toy_preprocess(cwd + '/toy/F2_B6_BTBR_OB_mice_clinic_traits.csv', cwd + '/toy/hypo_mlratio_final.csv')

#########################################################################################################


################ TODO: Import the model by calling a model function in models folder ####################
gene_input_shape = (len(X_train[0]),)
model = toy_model(gene_input_shape)
#########################################################################################################


#### TODO: Define the metrics we want to fit to (useful for tensorflow and non-tensorflow models) #######
metrics = [] # Wrap the metrics in the model file already 
#########################################################################################################

############# Train the model TODO #####################################################################
model.compile()
model.fit(X_train, y_train, 
          X_val,   y_val  ,
          )

########################################################################################################
# Evaluate the model after training. TODO
# Printing things will direct output to the .out file you specified in the CHTC submit script.
model.evaluate(X_test, y_test)
print(f'Test results - Loss: {model.test_result[0]} - model.test_results: {test_result[1]}')

########################################################################################################

########################################################################################################
# Save the results somewhere? For anything other than large model weight files, very simple.
#
# 
# Save the Model Paths (optional, might be too much if we are looping over
# hyper parameters)
# TODO: SEE STAGING OUTPUT FILE INSTRUCTIONS
# model_path = #TODO: Insert the place to save the weights if any
# model.save_weights(os.path.join(model_path, "cp_ckpt"))
#######################################################################################################
