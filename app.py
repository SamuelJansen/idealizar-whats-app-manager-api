import globals
globalsInstance = globals.newGlobalsInstance(__file__
    , settingStatus=True
    , successStatus = True
    , errorStatus = True
    , failureStatus = True
    # , debugStatus = True
    #
    # , warningStatus = True
    # , wrapperStatus = True
    # , logStatus = True
    # , testStatus = True
)

from python_framework import initialize, runApi
import IdealizarWhatsAppManagerApi
app = IdealizarWhatsAppManagerApi.app
api = IdealizarWhatsAppManagerApi.api
jwt = IdealizarWhatsAppManagerApi.jwt

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    runApi(debug=False, use_reloader=False)
    # app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)
