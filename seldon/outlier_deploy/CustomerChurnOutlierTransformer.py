import numpy as np
import joblib
import pandas as pd

class CustomerChurnOutlierTransformer(object):

    def __init__(self):
        self.encoder = joblib.load('CustomerChurnOutlierOrdinalEncoder.pkl')
        self.onehotencoder = joblib.load('CustomerChurnOutlierOneHotEncoder.pkl')
        self.featureslist = joblib.load('CustomerChurnFeaturesColumns.pkl')

    def transform_input(self, X, feature_names, meta):
        print (X)
        print (feature_names)
        df = pd.DataFrame(X, columns=feature_names)
        df = df.reindex(columns = self.featureslist)
        print(df)

#       df = df.drop(['customerID'], axis=1)
        df = self.encoder.transform(df)
        df = self.onehotencoder.transform(df)
        print (df.to_numpy())

        return df.to_numpy()
