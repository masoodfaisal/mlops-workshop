import joblib


class CustomerChurnDriftPredictor(object):

    def __init__(self):
        self.model = joblib.load('CustomerChurnDriftPredictor.sav')

    def predict(self, X, features_names):

        return self.model.predict(X)
