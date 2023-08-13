from flask import Flask, render_template
import os
from base64 import b64encode
import requests
import base64
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.environ['FLASK_APP_KEY']

CORS(app, origins=['http://localhost:8000', 'http://127.0.0.1:8000'])

# Get environment variables
APS_APP_ID = os.environ['APS_APP_ID']
APS_APP_SECRET = os.environ['APS_APP_SECRET']


# Views
#----------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth/2leggedtoken/')
def get_token():
    # get token for viewer
    data = get_2legged_token('viewables:read')
    return data


@app.route('/bucket-content/<bucket_name>/')
def get_bucket_content(bucket_name):
    """
    Retrieves objects in a bucket. It is only available to the bucket creator.
    
    Return: If request succeed, dict. with values: `bucketKey`, `objectId`, `objectKey`, `size`, etc.

    **Documentation: https://aps.autodesk.com/en/docs/data/v2/reference/http/buckets-:bucketKey-objects-GET/
    """
    # get token with scope data:read, to get bucket content
    token = get_2legged_token('data:read')['access_token']

    headers = { "Authorization" : "Bearer " + token }
    endpoint = f"https://developer.api.autodesk.com/oss/v2/buckets/{bucket_name}/objects"
    res = requests.get(endpoint, headers=headers)
    data = res.json()

    models = [{ 'model_title': model['objectKey'], 'model_urn': get_encoded_urn(model['objectId']), 'models_size': get_model_size(model['size']) } for model in data['items']]

    return models


# get token, depending on scope
def get_2legged_token(scope:str) -> dict:
    """
    Retrieves a two-legged token.
    
    Return: If request succeed, dict. with values: `access_token`, `expire_in`, `token_type`

    **Documentation: https://aps.autodesk.com/en/docs/oauth/v2/reference/http/gettoken-POST/
    """

    app_credentials = f'{APS_APP_ID}:{APS_APP_SECRET}'
    authorization_string = b64encode(bytes(app_credentials, 'utf-8')).decode('utf-8')
    headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept" : "application/json",
            "Authorization" : "Basic " + authorization_string
            }
    body = (f"grant_type=client_credentials&scope={scope}")   # scoper viewables:read allows Autodesk Viewer to show model

    res = requests.post("https://developer.api.autodesk.com/authentication/v2/token", data=body, headers=headers)
    data = res.json()
    return data

def get_encoded_urn(objectId):
    urn_bytes = base64.urlsafe_b64encode(objectId.encode("utf-8"))
    urn = str(urn_bytes, "utf-8")
    return urn.rstrip("=")

def get_model_size(size:int) -> str:
    return str(round(size/(1024**2), 2)) + 'Mb'

# Run app
#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8000)