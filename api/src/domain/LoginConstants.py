from python_helper import Constant as c
from python_helper import EnvironmentHelper
from python_framework import OpenApiManager
from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

STATIC_PATH_NAME = 'static'
STATIC_PACKAGE_PATH = f'{globalsInstance.baseApiPath}{STATIC_PATH_NAME}'

AUTHENTICATION_TEMPLATE_PACKAGE = f'authentication'
QR_CODE_IMAGE_NAME = f'{STATIC_PACKAGE_PATH}{EnvironmentHelper.OS_SEPARATOR}{AUTHENTICATION_TEMPLATE_PACKAGE}{EnvironmentHelper.OS_SEPARATOR}qr-code.png'
QR_CODE_TEMPLATE_NAME = f'{c.SLASH}{AUTHENTICATION_TEMPLATE_PACKAGE}{c.SLASH}qr-code.html'
QR_CODE_IMAGE_STATIC_PATH = f'{c.SLASH}{STATIC_PATH_NAME}{c.SLASH}{AUTHENTICATION_TEMPLATE_PACKAGE}{c.SLASH}qr-code.png'

QR_CODE_AUTHENTICATION_PAGE = f'{OpenApiManager.getApiUrl(globalsInstance.api)}/login/qr-code'
