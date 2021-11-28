class toy_model:

    def __init__(self, gene_input_shape):
        self.gene_input_shape = gene_input_shape
        self.model = create_model()
        self.test_result
        
    # Model creation
    def create_model():
        # Encoder gene expression data
        gene_encoder = layers.Input(shape=self.gene_input_shape, name='gene_input')
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
        
    # Training parameters
    def compile(loss = 'MeanSquaredError',opt="adam",metrics = metrics):
        self.model.compile(loss='MeanSquaredError', optimizer="adam", metrics=metrics)
             
    # Train
    def fit(X_train,y_train,X_val,y_val):
        model.fit(X_train, y_train, 
          epochs=50, batch_size=100, verbose=1, 
          validation_data=(X_val,y_val),
          #callbacks=[tensorboard_callback]
          )
          
    # Test
    def evaluate(X_test, y_test, verbose=1):
        self.test_result = model.evaluate(X_test, y_test, verbose=1)
        
        
    # Evaluation metric
    def pearson_corr(y_true, y_pred):   
        return tfp.stats.correlation(y_true,y_pred)

    def spearman_rankcor(y_true, y_pred):
        return ( tf.py_function(spearmanr, [tf.cast(y_pred, tf.float32), 
                       tf.cast(y_true, tf.float32)], Tout = tf.float32) )
