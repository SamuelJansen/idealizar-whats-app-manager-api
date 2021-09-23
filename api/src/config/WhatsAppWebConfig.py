from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL = globalsInstance.getApiSetting('idealizar.whats-app.web.base-url')
REQUEST_TIMEOUT = globalsInstance.getApiSetting('idealizar.whats-app.web.request-timeout')
