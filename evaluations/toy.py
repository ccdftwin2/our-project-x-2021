# Evaluation function for the toy model. I'm not sure if this is how we want to
# do it but is one option.
#

def pearson_corr(y_true, y_pred):
    
    return tfp.stats.correlation(y_true,y_pred)

# REQUIRES: from scipy.stats import spearmanr
def spearman_rankcor(y_true, y_pred):
     return ( tf.py_function(spearmanr, [tf.cast(y_pred, tf.float32), 
                       tf.cast(y_true, tf.float32)], Tout = tf.float32) )

