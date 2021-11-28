class toy_model:

    def __init__(self, gene_input_shape):
        self.gene_input_shape = gene_input_shape
        self.model = create_model()
        metrics=[
         "MeanAbsolutePercentageError",
         self.spearman_rankcor,
         self.pearson_corr
        ]
        self.test_result
        
    # Model creation
    def create_model():
    
        # Encoder gene expression data
        gene_encoder = layers.Input(shape=self.gene_input_shape, name='gene_input')
        gene_d1 = layers.Dense(5000, activation='relu',name='gene_d1',kernel_regularizer=tf.keras.regularizers.L2(0.03))(gene_encoder)
        gene_d1 = layers.Dropout(0.3)(gene_d1)
        gene_d2 = layers.Dense(1000, activation='relu',name='gene_d2',kernel_regularizer=tf.keras.regularizers.L2(0.03))(gene_d1)
        gene_d2 = layers.Dropout(0.3)(gene_d2)
        gene_d3 = layers.Dense(100, activation='relu',name='gene_d3',kernel_regularizer=tf.keras.regularizers.L2(0.03))(gene_d2)
        gene_d3 = layers.Dropout(0.3)(gene_d3)
        gene_d4 = layers.Dense(50, activation='relu',kernel_regularizer=tf.keras.regularizers.L2(0.03))(gene_d3)
        output = layers.Dense(1, activation='relu')(gene_d4)
        
        model = tf.keras.Model(inputs=[gene_encoder], outputs=[output])
 
        return model
        
    # Training parameters
    def compile(loss = 'MeanSquaredError',opt="adam",metrics = self.metrics):
        self.model.compile(loss='MeanSquaredError', optimizer=opt, metrics=metrics)
             
    # Train
    def fit(X_train,y_train,X_val,y_val):
        # Early stop call back
        callback_train = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)
        callback_val = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
        
        model.fit(X_train, y_train, 
          epochs=50, batch_size=100, verbose=1, 
          validation_data=(X_val,y_val),
          callbacks=[callback_train,callback_val]
          )
          
    # Test
    def evaluate(X_test, y_test, verbose=1):
        self.test_result = self.model.evaluate(X_test, y_test, verbose=1)
        
        
    # Evaluation Metric
    def pearson_corr(y_true, y_pred):   
        return tfp.stats.correlation(y_true,y_pred)

    def spearman_rankcor(y_true, y_pred):
        return ( tf.py_function(spearmanr, [tf.cast(y_pred, tf.float32), 
                       tf.cast(y_true, tf.float32)], Tout = tf.float32) )
