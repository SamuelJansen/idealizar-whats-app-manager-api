from python_framework import ResourceManager
import ModelAssociation

api, app, jwt = ResourceManager.initialize(__name__, ModelAssociation.MODEL)

# from flask_cors import CORS
# cors = CORS(app, resources={r"/*": {"origins": "*"}})

from flask import render_template
from python_helper import EnvironmentHelper
from domain import LoginConstants


from flask import make_response
from functools import wraps, update_wrapper
from datetime import datetime

# def nocache(view):
#     @wraps(view)
#     def no_cache(*args, **kwargs):
#         response = make_response(view(*args, **kwargs))
#         response.headers['Last-Modified'] = datetime.now()
#         response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
#         response.headers['Pragma'] = 'no-cache'
#         response.headers['Expires'] = '-1'
#         return response
#
#     return update_wrapper(no_cache, view)

@app.route(f'{api.baseUrl}/login/qr-code')
# @nocache
def authenticationQRCode():
    return render_template(LoginConstants.QR_CODE_TEMPLATE_NAME, data=LoginConstants.QR_CODE_IMAGE_STATIC_PATH)

# from flask import Flask, jsonify, request
# from io import BytesIO
# import base64
# import re
# import json
# from PIL import Image
#
# @app.route(f'{api.baseUrl}/process_image', methods=['POST'])
# def process_image():
#     image_data = request.get_json()['image'] ###-re.sub('^data:image/.+;base64,', '', request.form['data']['image'])
#     # print(image_data)
#     im = Image.open(BytesIO(base64.b64decode(image_data)))
#     im.save(LoginConstants.QR_CODE_IMAGE_NAME)
#     from python_framework import WebBrowser
#     import webbrowser
#     webbrowser.get('C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s --incognito').open(f'http://localhost:5500{api.baseUrl}/login/qr-code')
#     return json.dumps({'result': 'success'}), 200, {'ContentType': 'application/json'}
