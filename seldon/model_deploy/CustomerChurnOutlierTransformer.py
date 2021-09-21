import numpy as np
import joblib
import pandas as pd

class CustomerChurnOutlierTransformer(object):

    def __init__(self):
        self.encoder = joblib.load('CustomerChurnOutlierOrdinalEncoder.pkl')
        self.onehotencoder = joblib.load('CustomerChurnOutlierOneHotEncoder.pkl')

    def transform_input(self, X, feature_names, meta):

        df = pd.DataFrame(X, columns=feature_names)
        df = self.encoder.transform(df)
        df = self.onehotencoder.transform(df)
        return df.to_numpy()
