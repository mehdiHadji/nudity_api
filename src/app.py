import logging
import os
import sys

import tensorflow as tf
from flask import Flask, request, jsonify
from keras.models import load_model


from src.helpers.functions import load_input, transform_input, predict

tf.get_logger().setLevel('ERROR')
os.environ["KMP_WARNINGS"] = "FALSE"

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.logger.setLevel(logging.ERROR)

IMAGE_LENGTH = 128
MODEL_PATH = '/src/pkl_objects/model.hdf5'
MODEL_PATH = 'src/pkl_objects/model.hdf5'

graph = None
classifier = None


def load_model_():
    global graph
    global classifier

    print("######## SYS", sys.path)

    classifier = load_model(filepath=MODEL_PATH)
    classifier._make_predict_function()
    graph = tf.get_default_graph()


@app.route("/")
def home():
    return jsonify(isError=False, message="Success", statusCode=200, data="API IS WORKING"), 200


@app.route('/predictNudityByUrl', methods=['POST'])
def checkNudityV2():
    try:
        received_input = load_input(request.get_json()['url'])
        transformed_input = transform_input(input_image=received_input, img_length=IMAGE_LENGTH)

        # src: https://github.com/keras-team/keras/issues/10431
        with graph.as_default():
            result = predict(input_classifier=classifier, input_entry=transformed_input)

        return jsonify(isError=False, message="Success", statusCode=200, prediction=result), 200

    except Exception as e:
        app.logger.error(str(e))
        return jsonify(isError=True, message="Failure", statusCode=400, traceback=str(e)), 400


if __name__ == "__main__":
    load_model_()
    app.run(host='0.0.0.0', port=5002, debug=True)
