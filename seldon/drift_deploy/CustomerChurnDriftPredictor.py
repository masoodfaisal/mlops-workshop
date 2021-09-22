import joblib
from alibi_detect.utils.saving import load_detector
import pandas as pd

class CustomerChurnDriftPredictor(object):

    def __init__(self):
        self.model = joblib.load('CustomerChurnDriftPredictor.sav')
        self.model = load_detector('CustomerChurnDriftPredictor')
        # self.model = load_detector('CustomerChurnDriftPredictor')
    def predict(self, X, features_names):
        print (X)
        print(X[0].dtype)
        print(X.dtype)
        print (features_names)
        X = X.astype(object)
        print (X.dtype)
        #parse the non categorical fields to numbers
        senior_citizen_index = features_names.index('SeniorCitizen')
        tenure_index = features_names.index('tenure')
        monthly_charges_index = features_names.index('MonthlyCharges')
        total_charges_index = features_names.index('TotalCharges')
        print (senior_citizen_index,tenure_index,monthly_charges_index,total_charges_index)
        print (X[0][senior_citizen_index])
        X[0][senior_citizen_index] = float(X[0][senior_citizen_index])
        print (X[0][senior_citizen_index])
        X[0][tenure_index] = int(X[0][tenure_index])
        X[0][monthly_charges_index] = float(X[0][monthly_charges_index])
        X[0][total_charges_index] = float(X[0][total_charges_index])
        print(X.shape)
        # X_ = pd.DataFrame(X)
        return self.model.predict(X.astype(object))
