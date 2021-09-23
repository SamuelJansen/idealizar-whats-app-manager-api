from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL = globalsInstance.getApiSetting('idealizar.agenda.base-url')
REQUEST_TIMEOUT = int(globalsInstance.getApiSetting('idealizar.agenda.request-timeout'))
