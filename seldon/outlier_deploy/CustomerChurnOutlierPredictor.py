import joblib


class CustomerChurnOutlierPredictor(object):

    def __init__(self):
        self.model = joblib.load('CustomerChurnOutlierPredictor.sav')

    def predict(self, X, features_names):
        return self.model.predict(X)
