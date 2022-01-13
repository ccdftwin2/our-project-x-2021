import tensorflow as tf
from tensorflow.keras import layers

def re_toy_model(gene_input_shape,drop_out_rate = 0.3, l2_r = 0.5,first_layer_unit_num=10000):
    
    # Encoder gene expression data
    gene_encoder = layers.Input(shape=gene_input_shape, name='gene_input')
    gene_d1 = layers.Dense(first_layer_unit_num, activation='relu',name='gene_d1',kernel_regularizer=tf.keras.regularizers.L2(l2_r))(gene_encoder)
    gene_d1 = layers.Dropout(drop_out_rate)(gene_d1)
    gene_d2 = layers.Dense(5000, activation='relu',name='gene_d2',kernel_regularizer=tf.keras.regularizers.L2(l2_r))(gene_d1)
    gene_d2 = layers.Dropout(drop_out_rate)(gene_d2)
    gene_d3 = layers.Dense(1000, activation='relu',name='gene_d3',kernel_regularizer=tf.keras.regularizers.L2(l2_r))(gene_d2)
    gene_d3 = layers.Dropout(drop_out_rate)(gene_d3)
    gene_d4 = layers.Dense(100, activation='relu',kernel_regularizer=tf.keras.regularizers.L2(l2_r))(gene_d3)
    output = layers.Dense(1, activation='relu')(gene_d4)
    
    model = tf.keras.Model(inputs=[gene_encoder], outputs=[output])
 
    return model