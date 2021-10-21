# Import all the libraries we need.
import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
import tensorflow as tf
import tensorflow_probability as tfp
import datetime
import os

# IMPORT THE FUNCTIONS WE NEED FROM MODEL AND EVALUATION TODO
#os.chdir("**Put here the directory where you have the file with your function**")
#from file import function

#os.chdir("**Put here the directory where you have the file with your function**")
#from file2 import function2, function3

os.chdir(***path to toy dataprocessing script***)
from ***path to toy dataprocessing script*** import toy_preprocess

os.chdir(***path to toy model script***)
from ***path to toy model script***) import toy_model

os.chdir(***path to evaluations**)
from **path to toy evaluations scripts***) import eval1, eval2, ...
#os.chdir("**Put here the directory where you were working**")

# TODO: Read in the arguments from the CHTC script. This will be important for 
# hyperparameter tuning

# TODO: Run the preprocessing script
# The data paths will be data on the staging data file systems
# Will have lots of outputs if using cross-validation
X_train, sex_train, y_train, X_val, sex_val, y_val, X_test, sex_test, y_test \
    = toy_preprocess(***insert path to hypo here***, **path to clinical here**)

# TODO: Import the model by calling a model function in models folder
gene_input_shape = (len(X_train[0]),)
model =toy_model(gene_input_shape)

# TODO: Define the metrics we want to fit to (tensorflow only)
metrics = []

# Train the model TODO: Might be tensorflow, might not be
model.compile(loss='MeanSquaredError', optimizer="adam", metrics=metrics)
model.fit([X_train,sex_train], y_train, 
          epochs=50, batch_size=100, verbose=1, 
          validation_data=([X_val,sex_val],y_val),
          #callbacks=[tensorboard_callback]
          )

# Evaluate the model after training. TODO: Change to evaluation folder
test_results = model.evaluate([X_test,sex_test], y_test, verbose=1)
print(f'Test results - Loss: {test_results[0]} - mean_absolute_percentage_error: {test_results[1]}')
# Save the results somewhere?

# Save the Model Paths (optional, might be too much if we are looping over
# hyper parameters)
model_path = #TODO: Insert the place to save the weights if any
model.save_weights(os.path.join(model_path, "cp_ckpt"))
