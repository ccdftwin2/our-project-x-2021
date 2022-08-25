# Evaluation function for the toy model. I'm not sure if this is how we want to
# do it but is one option.
#

import tensorflow as tf
import tensorflow_probability as tfp
from scipy.stats import spearmanr

def pearson_corr(y_true, y_pred):
    
    return tfp.stats.correlation(y_true,y_pred)

# REQUIRES: from scipy.stats import spearmanr
from scipy.stats import spearmanr
def spearman_four(y_true, y_pred):
  result = 0.0
  for i in range(4):
    result += spearmanr(y_true[:,i], y_pred[:,i])[0]
  return result/4.0
def spearman_rankcor(y_true, y_pred):
  return ( tf.py_function(spearman_four, [tf.cast(y_pred, tf.float64), 
    tf.cast(y_true, tf.float64)], Tout = tf.float64) )
