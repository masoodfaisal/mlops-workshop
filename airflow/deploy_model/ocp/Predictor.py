import joblib
import pandas as pd
import numpy as np
from alibi_detect.utils.saving import load_detector
import json

class Predictor(object):

    def __init__(self):
        self.model = joblib.load('model.pkl')


    def predict_raw(self, request):
        data = request.get("data", {}).get("ndarray")
        mult_types_array = np.array(data, dtype=object)

        result = self.model.predict(mult_types_array)

        return json.dumps(result, cls=JsonSerializer)

class JsonSerializer(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (
        np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
