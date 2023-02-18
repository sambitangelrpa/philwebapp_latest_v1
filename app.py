import json
from flask import Flask,jsonify,send_file
from flask.wrappers import Response
from flask.globals import request, session
import requests
from flask_cors import CORS
from send_s3_link import send_s3_function
import os




app = Flask(__name__)

CORS(app)
app.config['Access-Control-Allow-Origin'] = '*'
app.config["Access-Control-Allow-Headers"]="Content-Type"
app.config['SECRET_KEY'] = 'mysecretkey'
# bypass http
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

@app.route('/api/fed_prediction')
def fed_prediction():
    # Get the S3 object URL
    fed_pred_obj=send_s3_function()
    link=fed_pred_obj.get_fed_prediction_link()

    # Return the URL as a JSON response
    return jsonify({'fed_prediction': link})


@app.route('/api/ecb_prediction')
def ecb_prediction():
    # Get the S3 object URL
    ecb_prediction_obj = send_s3_function()
    link = ecb_prediction_obj.get_ecb_prediction_link()

    # Return the URL as a JSON response
    return jsonify({'ecb_prediction': link})


@app.route('/api/boe_prediction')
def boe_prediction():
    # Get the S3 object URL
    boe_prediction_obj = send_s3_function()
    link = boe_prediction_obj.get_boe_prediction_link()

    # Return the URL as a JSON response
    return jsonify({'boe_prediction': link})

@app.route('/api/fed_wordcloud')
def fed_wordcloud():
    # Get the S3 object URL
    fed_wordcloud_obj = send_s3_function()
    link = fed_wordcloud_obj.get_fed_wordcloud_zip()

    # Return the URL as a JSON response
    return jsonify({'fed_wordcloud': link})

@app.route('/api/ecb_wordcloud')
def ecb_wordcloud():
    # Get the S3 object URL
    ecb_wordcloud_obj = send_s3_function()
    link = ecb_wordcloud_obj.get_ecb_wordcloud_zip()

    # Return the URL as a JSON response
    return jsonify({'ecb_wordcloud': link})

@app.route('/api/boe_wordcloud')
def boe_wordcloud():
    # Get the S3 object URL
    boe_wordcloud_obj = send_s3_function()
    link = boe_wordcloud_obj.get_boe_wordcloud_zip()

    # Return the URL as a JSON response
    return jsonify({'boe_wordcloud': link})

if __name__ == "__main__":

    app.run()