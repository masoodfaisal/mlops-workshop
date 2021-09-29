import joblib
import tensorflow as tf 
import numpy as np
# import tensorflow_hub as hub
import json
# from PIL import Image
# import io
# from urllib import request

class ImageClassificationPredictor(object):

    def __init__(self):
        self.model = tf.keras.models.load_model('ImageClassificationPredictor.h5')#,compile=False)#
        self.class_name = joblib.load('ImageClassificationClassNames.pkl')


    def predict_raw(self, request):
        print(request.get("data", {}))
        img_path = request.get("data", {}).get("path")
        print(img_path[0])

        # Download label map file and image
        # labels_map = '/tmp/imagenet1k_labels.txt'
        image_file = '/tmp/img.jpg'
        tf.keras.utils.get_file(image_file, str(img_path[0]))

        # preprocess image.
        image = tf.keras.preprocessing.image.load_img(image_file, target_size=(224, 224))
        img_array = tf.keras.preprocessing.image.img_to_array(image)
        img_array = (img_array - 128.) / 128.
        img_array = tf.expand_dims(img_array, 0)
        print(img_array.shape)

        # predictions = self.model.predict(img_array)

        predictions = self.model(img_array, training=False)
        print(predictions)
        score = tf.nn.softmax(predictions[0])
        print(score)
        class_label = self.class_name[np.argmax(score)]
        print(class_label)
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