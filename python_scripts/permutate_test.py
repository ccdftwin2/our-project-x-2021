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
# from individual_preprocess import preprocess_cv
# from toy_preprocess import five_tissues_preprocess,five_tissues_preprocess_cv
from new_CV import preprocess_cv

# For the toy model script
from flex_nn_model import flex_nn_model

# For the toy evaluations scripts
from toy_eval import pearson_corr, spearman_rankcor, spearman_four

# Change back to the current working directory
print(cwd)
os.chdir(cwd)
print(cwd)
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

X_train, y_train , _ , X_test , y_test \
    = preprocess_cv(cwd + "/"+tissue+"/"+data_genes, cwd +"/" +tissue+"/"+  data_gluc, cwd +"/"+tissue+"/"+ data_sex)
#########################################################################################################

print(X_train.shape,y_train.shape,X_test.shape,y_test.shape)
################ TODO: Import the model by calling a model function in models folder ####################
gene_input_shape = (len(X_train[0]),)
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

#X_train = np.array([X[i] for i in index[0]])
#y_train = np.array([y[i] for i in index[0]])
#X_test = np.array([X[i] for i in index[1]])
#y_test = np.array([y[i] for i in index[1]])

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

# load the model
cwd = os.getcwd()
print(cwd)
#model.load_weights(os.path.join(cwd, "cp.cpkt"))
model.fit(X_train, y_train, 
          epochs=100, batch_size=batch_size, verbose=1, 
          validation_split = 0.15,
          callbacks=[callback_train,callback_val]
          )
####################################################################################################
# Evaluate the model after training. TODO
# Printing things will direct output to the .out file you specified in the CHTC submit script.

test_results = model.evaluate(X_test, y_test, verbose=1)

# save results
model.save_weights(os.path.join(cwd, "cp.cpkt"))

exit()

import pickle

with open(os.path.join(cwd, tissue+'_indices.pkl'), 'rb') as f:
    modules = pickle.load(f)

discrepency = [[] for i in range(len(modules.keys()))]# record the discrepency after permute a module for certain iterations
suc = 5 # how many iterations we want to see the "success"
upper = 25 # the maximun iterations we want to run

counter1 = 0 # count the number of success for first metric
counter2 = 0 # count the number of success for second metric

for i,key in enumerate(modules.keys()):
  print(key)
  X_test_copy = np.array(X_test.copy())
  for j in range(upper):  
    for col_index in modules[key]:
      np.random.shuffle(X_test_copy[:,col_index]) # permute the transcripts   
    '''
    your testing after permutation goes here
    '''
    # -------------- Use neural net as a example ------------------------
    per_result = np.array(model.evaluate(X_test_copy, np.array(y_test), verbose=0))
    discrepency[i].append(per_result - test_results) 

    if per_result[1] > test_results[1]:
      counter1+=1
    if per_result[2]**2 > test_results[2]**2:
      counter2+=1
    if counter1 >= suc and counter2 >= suc:
      break
  # reset the counter
  counter1 = 0
  counter2 = 0

outf = open(os.path.join(cwd, tissue+"_modules_details.csv"),"w")
csvwriter =csv.writer(outf, delimiter=',')
for i,key in enumerate(modules.keys()):
    csvwriter.writerow([key]+list(discrepency[i])) 
outf.close()

output = open(os.path.join(cwd, tissue+"_modules.csv"), "w")
csvwriter =csv.writer(output, delimiter=',')
csvwriter.writerow(["Standard"]+list(test_results))
for i,key in enumerate(modules.keys()):
    csvwriter.writerow([key]+list(np.mean(discrepency[i],axis=0)))
output.close()





