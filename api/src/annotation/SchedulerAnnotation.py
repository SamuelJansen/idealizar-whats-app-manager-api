from python_helper import Constant as c
from python_helper import ReflectionHelper, ObjectHelper, log, Function
from python_framework import FlaskManager

apiInstance = FlaskManager.getApi()

@Function
def Scheduler() :
    def Wrapper(OuterClass, *args, **kwargs):
        log.debug(Scheduler,f'''wrapping {OuterClass.__name__}''')
        class InnerClass(OuterClass):
            def __init__(self,*args,**kwargs):
                log.debug(OuterClass,f'in {InnerClass.__name__}.__init__(*{args},**{kwargs})')
                OuterClass.__init__(self,*args,**kwargs)
                self.globals = apiInstance.globals
                self.service = apiInstance.resource.service
        ReflectionHelper.overrideSignatures(InnerClass, OuterClass)
        return InnerClass
    return Wrapper

@Function
def SchedulerMethod(*methodArgs, requestClass=None, **methodKwargs) :
    def innerMethodWrapper(resourceInstanceMethod, *innerMethodArgs, **innerMethodKwargs) :
        log.debug(SchedulerMethod,f'''wrapping {resourceInstanceMethod.__name__}''')
        methodClassName = ReflectionHelper.getMethodClassName(resourceInstanceMethod)
        methodName = ReflectionHelper.getName(resourceInstanceMethod)
        shedulerId = methodKwargs.get('id', f'{methodClassName}{c.DOT}{methodName}')
        maxInstances =  methodKwargs.get('max_instances', 1)
        methodKwargs['id'] = shedulerId
        methodKwargs['max_instances'] = maxInstances
        @apiInstance.scheduler.task(*methodArgs, **methodKwargs)
        def innerResourceInstanceMethod(*args, **kwargs) :
            args = getArgumentInFrontOfArgs(args, ReflectionHelper.getAttributeOrMethod(apiInstance.resource.scheduler, methodClassName[:-len('Scheduler')].lower()))
            resourceInstance = args[0]
            methodReturn = None
            try :
                FlaskManager.validateArgs(args,requestClass,innerResourceInstanceMethod)
                methodReturn = resourceInstanceMethod(*args,**kwargs)
            except Exception as exception :
                FlaskManager.raiseGlobalException(exception, resourceInstance, resourceInstanceMethod)
                log.log(innerResourceInstanceMethod, f'Not possible to run {shedulerId} properly', exception=exception)
            return methodReturn
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper

@Function
def getArgumentInFrontOfArgs(args, argument) :
    return [argument, *args]