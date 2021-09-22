import joblib
from alibi_detect.utils.saving import load_detector
import pandas as pd
import json
import numpy as np

class CustomerChurnDriftPredictor(object):

    def __init__(self):
        self.model = joblib.load('CustomerChurnDriftPredictor.sav')
        # self.model = load_detector('CustomerChurnDriftPredictor')
        # self.model = load_detector('CustomerChurnDriftPredictor')

    def predict(self, X, features_names):
        X = X.astype(object)
        X[0][1] = int(X[0][1])
        X[0][4] = int(X[0][4])
        X[0][17] = float(X[0][17])
        X[0][18] = float(X[0][18])
        # p = self.model.predict(X)
        return json.dumps(self.model.predict(X), cls=NumpyEncoder)






class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (
        np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)




# import joblib
# import numpy as np
# import json

# class CustomerChurnDriftPredictor(object):

#     def __init__(self):
#         self.model = joblib.load('CustomerChurnDriftPredictor.sav')

#     def predict(self, X, features_names):
#         X = X.astype(object)
#         X[0][1] = int(X[0][1])
#         X[0][4] = int(X[0][4])
#         X[0][17] = float(X[0][17])
#         X[0][18] = float(X[0][18])
#         # p = self.model.predict(X)
#         return json.dumps(self.model.predict(X), cls=NumpyEncoder)




# class NumpyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, (
#         np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
#             return int(obj)
#         elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
#             return float(obj)
#         elif isinstance(obj, (np.ndarray,)):
#             return obj.tolist()
#         return json.JSONEncoder.default(self, obj)
        




        # for idx, data in np.ndenumerate(X[0]):
        #     print(X[0][idx])
        #     X[0][idx] = converter.convert(data)
        #     print(converter.convert(data))

