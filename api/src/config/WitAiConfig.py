from globals import getGlobalsInstance
globalsInstance = getGlobalsInstance()

BASE_URL =  globalsInstance.getApiSetting('wit-ai.base-url')
AUTHORIZATION = f'Bearer {globalsInstance.getApiSetting("wit-ai.authorization")}'
APP_ID = globalsInstance.getApiSetting("wit-ai.app-version")
