def toy_model(gene_input_shape):

  # Encoder gene expression data
  gene_encoder = layers.Input(shape=gene_input_shape, name='gene_input')
  gene_d1 = layers.Dense(1000, activation='relu',name='gene_d1')(gene_encoder)
  gene_d2 = layers.Dense(500, activation='relu',name='gene_d2')(gene_d1)
  gene_d3 = layers.Dense(100, activation='relu',name='gene_d3')(gene_d2)

  # Encoder for sex
  sex_encoder = layers.Input(shape=(1,), name='sex_input')
  sex_embed = layers.Embedding(2, 200)(sex_encoder)
  sex_d1 = layers.Dense(100, activation='relu',name='sex_d1')(sex_embed)
  sex_d1 = layers.Reshape((100,))(sex_d1)

  # Combine two features
  Concat = layers.Concatenate(name='concat')([gene_d3, sex_d1])
  Concat_d1 = layers.Dense(100, activation='relu')(Concat)
  Concat_d2 = layers.Dense(50, activation='relu')(Concat_d1)
  output = layers.Dense(1, activation='relu')(Concat_d2)

  model = tf.keras.Model(inputs=[gene_encoder,sex_encoder], outputs=[output])

  return model

