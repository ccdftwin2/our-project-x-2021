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
from toy_model import toy_model

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
model =toy_model(gene_input_shape)
#########################################################################################################


#### TODO: Define the metrics we want to fit to (useful for tensorflow and non-tensorflow models) #######
metrics = []
#########################################################################################################

############# Train the model TODO #####################################################################
model.compile(loss='MeanSquaredError', optimizer="adam", metrics=metrics)
model.fit([X_train,sex_train], y_train, 
          epochs=50, batch_size=100, verbose=1, 
          validation_data=([X_val,sex_val],y_val),
          #callbacks=[tensorboard_callback]
          )

########################################################################################################
# Evaluate the model after training. TODO
# Printing things will direct output to the .out file you specified in the CHTC submit script.
test_results = model.evaluate([X_test,sex_test], y_test, verbose=1)
print(f'Test results - Loss: {test_results[0]} - mean_absolute_percentage_error: {test_results[1]}')

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
