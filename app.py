import globals
globalsInstance = globals.newGlobalsInstance(__file__
    , settingStatus = True
    , successStatus = True
    , errorStatus = True
    , debugStatus = True
    , failureStatus = True

    , warningStatus = True
    , wrapperStatus = True
    , logStatus = True
    # , testStatus = True
)

from python_framework import initialize
import IdealizarWhatsAppManagerApi
app = IdealizarWhatsAppManagerApi.app
api = IdealizarWhatsAppManagerApi.api
jwt = IdealizarWhatsAppManagerApi.jwt

from python_helper import Constant as c
from python_helper import EnvironmentHelper
from flask_apscheduler import APScheduler
# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
scheduler.api_enabled = True if c.TRUE == EnvironmentHelper.get('SCHEDULER_API_ENABLED') else False
scheduler.init_app(app)
scheduler.start()

from python_framework import ResourceManager
api.scheduler = scheduler

api.resource.scheduler = ResourceManager.FlaskResource()
import PoolerScheduler
api.resource.scheduler.pooler = PoolerScheduler.PoolerScheduler()

@initialize(api, defaultUrl = '/swagger', openInBrowser=False)
def runFlaskApplication(app):
    app.run(debug=False, use_reloader=False)
    # app.run(debug=True)

if __name__ == '__main__' :
    runFlaskApplication(app)


# api.scheduler.shutdown(shutdown_threadpool=False)
import atexit
atexit.register(lambda: api.scheduler.shutdown(wait=False))
