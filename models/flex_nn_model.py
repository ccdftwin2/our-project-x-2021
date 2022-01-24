import tensorflow as tf
from tensorflow.keras import layers

def flex_nn_model(gene_input_shape, l2_r, drop_out_rates, act, num_layers, size_layers):
    
    gene_encoder = layers.Input(shape=gene_input_shape, name='gene_input')
    tmp = gene_encoder
    
    for i in range(num_layers):
        cur = layers.Dense(size_layers[i], activation=act, name='gene_d'+str(i+1), kernel_regularizer=tf.keras.regularizers.L2(l2_r))(tmp)
        cur = layers.Dropout(drop_out_rates[i])(cur)
        tmp = cur
        
    output = layers.Dense(1, activation=act)(tmp)
    # Encoder gene expression data
    model = tf.keras.Model(inputs=[gene_encoder], outputs=[output])
 
    return model
