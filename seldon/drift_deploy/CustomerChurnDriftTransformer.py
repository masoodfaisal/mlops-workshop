import numpy as np
import joblib
import pandas as pd

class CustomerChurnDriftTransformer(object):
    def transform_input(self, X, feature_names, meta):
        # print(X)
        # print(feature_names)
        # print(meta)
        df = pd.DataFrame(X, columns=feature_names)

        df = df.drop(['customerID'], axis=1)
        # print(df.to_numpy())
        return df.to_numpy()
