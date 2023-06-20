import urllib

import numpy as np
from keras.preprocessing import image


def downloadImage(url: str) -> str:
    urllib.request.urlretrieve(url, 'image.jpg')
    return 'image.jpg'


def load_input(url: str) -> str:
    return downloadImage(url)


def transform_input(input_image, img_length):
    img_tensor = np.expand_dims(
        image.img_to_array(
            image.load_img(input_image, target_size=(img_length, img_length, 3))), axis=0
    ) / 255.

    return img_tensor


def predict(input_classifier, input_entry: np.ndarray) -> dict:
    pred_prob = input_classifier.predict(input_entry)[0][0]
    pred_class = input_classifier.predict_classes(input_entry)[0][0]

    return {
        'is_nude': list(map(lambda x: False if x == 1 else True, [pred_class]))[0],
        'confidence': round(pred_prob * 100, 3)
    }
