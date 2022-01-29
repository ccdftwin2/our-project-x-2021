# Import all the libraries we need.
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
import tensorflow as tf
import tensorflow_probability as tfp
import datetime
import os
from scipy.stats import spearmanr
import csv

# Variable for the current directory
cwd = os.getcwd()

#################### IMPORT THE FUNCTIONS WE NEED FROM MODEL AND EVALUATION TODO ####################
#os.chdir("**Put here the directory where you have the file with your function**")
#from file import function

#os.chdir("**Put here the directory where you have the file with your function**")
#from file2 import function2, function3

# For the toy dataprocessing
from individual_preprocess import preprocess_cv
from toy_preprocess import five_tissues_preprocess,five_tissues_preprocess_cv

# For the toy model script
from flex_nn_model import flex_nn_model

# For the toy evaluations scripts
from toy_eval import pearson_corr, spearman_rankcor, spearman_four

# Change back to the current working directory
os.chdir(cwd)
#########################################################################################################

try:
    # Disable all GPUS
    tf.config.set_visible_devices([], 'GPU')
    visible_devices = tf.config.get_visible_devices()
#    for device in visible_devices:
#        assert device.device_type != 'GPU'
except:
    # Invalid device or cannot modify virtual devices once initialized.
    pass

# Assign variables for all the hyperparameters that we could tune
momentum = 0.9
data_genes = ""
data_gluc = ""
data_sex = ""
l2_r = 0.5
batch_size = 10
learning_rate = 0.1
my_opt = "adam" # optimizers (adam, adagrad, RMSprop)
num_layers = 4
size_layers = []
drop_out_rates = []
patience = 3
act = "swish"

# Get the arguments
if __name__ == "__main__":	
    run_id = str(sys.argv[1])
    path = str(sys.argv[2])
    tissue = str(sys.argv[4])
    file_in = str(sys.argv[3])

    #print(f"Arguments count: {len(sys.argv)}")
    #for i, arg in enumerate(sys.argv):
    #    print(f"Argument {i:>6}: {arg}")

my_file_in = open(run_id + ".in","r")
args = my_file_in.readline().split(',')
organ = str(args[0])
data_genes = str(args[1])
data_gluc = str(args[2])
data_sex = str(args[3])
momentum = float(args[4])
l2_r = float(args[5])
batch_size = int(args[6])
learning_rate = float(args[7])
my_opt = str(args[8])
num_layers = int(args[9])
pat = int(args[10])
run_id = str(args[11])

# Get the size of layers and drop out rates
for i in range(num_layers):
    size_layers.append(int(args[12+i]))
for i in range(num_layers):
    drop_out_rates.append(float(args[12+num_layers+i]))
    
print("Run id:", run_id)
########### TODO: Read in the arguments from the CHTC script. ###########################################
# This will be important for hyperparameter tuning. No arguments for toy script.
# TODO: Run the preprocessing script to get the dataset
# The data paths will be IN THE CURRENT WORKING DIRECTORY (see toy.sh)
# Will have lots of outputs if using cross-validation

mirrored_strategy = tf.distribute.MirroredStrategy()

with mirrored_strategy.scope():
    X, y , sex , indices \
        = preprocess_cv(cwd + "/"+tissue+"/"+data_genes, cwd +"/" +tissue+"/"+  data_gluc, cwd +"/"+tissue+"/"+ data_sex)
    #########################################################################################################


    ################ TODO: Import the model by calling a model function in models folder ####################
    gene_input_shape = (len(X[0]),)
    model = flex_nn_model(gene_input_shape, l2_r, drop_out_rates, act, num_layers, size_layers)
    #########################################################################################################


    #### TODO: Define the metrics we want to fit to (useful for tensorflow and non-tensorflow models) #######
    metrics = [
             "MeanAbsolutePercentageError",
             spearman_rankcor,
             pearson_corr
            ]
    ########################################################################################################

    ############# Train the model TODO #####################################################################
    callback_train = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=pat)
    callback_val = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)


    results = []
    # Cross validation code
    for j,index in enumerate(indices):

        print("CV:",j,"------------------------------------")

        X_train = np.array([X[i] for i in index[0]])
        y_train = np.array([y[i] for i in index[0]])

        X_test = np.array([X[i] for i in index[1]])
        y_test = np.array([y[i] for i in index[1]])
        
        # Choose between different optimizers
        if my_opt == "adam":
            model.compile(loss='MeanSquaredError', optimizer=tf.keras.optimizers.Adam(learning_rate), \
             metrics=metrics)
        if my_opt == "adagrad":
            model.compile(loss='MeanSquaredError', optimizer=tf.keras.optimizers.Adagrad(learning_rate), \
             metrics=metrics)
        if my_opt == "RMSprop":
            model.compile(loss='MeanSquaredError', optimizer=tf.keras.optimizers.RMSprop(learning_rate), \
             metrics=metrics)

        # fit the model
        model.fit(X_train, y_train, 
                  epochs=100, batch_size=batch_size, verbose=1, 
                  #validation_data=(X_val,y_val),
                  validation_split = 0.15,
                  callbacks=[callback_train,callback_val]
                  )

        ####################################################################################################
        # Evaluate the model after training. TODO
        # Printing things will direct output to the .out file you specified in the CHTC submit script.
        print("BEGIN testing-------------------")
        test_results = model.evaluate(X_test, y_test, verbose=1)
        results.append(test_results)

# save results
results = np.array(results)
print("loss:", np.mean(results[:,0]),"abs%:", np.mean(results[:,1]),
"spearman:", np.mean(results[:,2]),"pearson:", np.mean(results[:,3]))

parent = os.getcwd() + "/" + "results"
if not os.path.exists(parent):
    os.mkdir(parent)
path = os.path.join(parent, tissue)
if not os.path.exists(path):
    os.mkdir(path)

print("loss:", np.mean(results[:,0]),"abs%:", np.mean(results[:,1]),"spearman:", np.mean(results[:,2]),"pearson:", np.mean(results[:,3]))


avg = np.round(np.mean(results,axis=0),4)
str_avg = str(avg[0])
for i in range(3):
    str_avg = str_avg + "," + str(avg[i+1])
print(str_avg)
for i in range(len(results)):
    tmp_str = str(results[i][0])
    for j in range(3):
        tmp_str = tmp_str + "," + str(results[i][1+j])
    print(tmp_str)
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


