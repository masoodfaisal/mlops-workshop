import joblib
import tensorflow as tf 
import numpy as np
import tensorflow_hub as hub
import json
from PIL import Image
import io
from urllib import request

class ImageClassificationPredictor(object):

    def __init__(self):
        self.model = tf.keras.models.load_model('ImageClassificationPredictor.h5',custom_objects={'KerasLayer':hub.KerasLayer})#,compile=False)#
        self.class_name = joblib.load('ImageClassificationClassNames.pkl')


    def predict_raw(self, request1):
        print(request1.get("data", {}))
        img_path = request1.get("data", {}).get("path")
        print(img_path[0])

        res = request.urlopen(str(img_path[0])).read()
        img_array = Image.open(io.BytesIO(res)).resize((224, 224))
        # img = tf.keras.preprocessing.image.load_img(str(img_path[0]), target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(img_array)
        img_array = img_array/255
        img_array = tf.expand_dims(img_array, 0) # Create a batch

        # predictions = self.model.predict(img_array)

        predictions = self.model(img_array, training=False)
        score = tf.nn.softmax(predictions[0])
        class_label = self.class_name[np.argmax(score)]
        conf = 100 * np.max(score)
        results = [class_label,conf]
        print(results)
        # print(
        #     "This image most likely belongs to {} with a {:.2f} percent confidence."
        #     .format(self.class_name[np.argmax(score)], 100 * np.max(score))
        # )
        # return results
        return json.dumps(results, cls=JsonSerializer)

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