from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL = globalsInstance.getApiSetting('whats-app.web.base-url')
REQUEST_TIMEOUT = globalsInstance.getApiSetting('whats-app.web.request-timeout')
