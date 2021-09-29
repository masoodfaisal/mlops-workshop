import numpy as np
import joblib
import pandas as pd

class Transformer(object):
    def transform_input(self, X, feature_names, meta):
        df = pd.DataFrame(X, columns=feature_names)
        
        #df = df.drop(['customerID'], axis=1)
        return df.to_numpy()
