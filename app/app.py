from flask import Flask, render_template
import os
from base64 import b64encode
import requests

app = Flask(__name__)


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
    body = ("grant_type=client_credentials&scope=viewables:read")   # scoper viewables:read allows Autodesk Viewer to show model

    res = requests.post("https://developer.api.autodesk.com/authentication/v2/token", data=body, headers=headers)
    data = res.json()

    return data


# Run app
#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=8000)