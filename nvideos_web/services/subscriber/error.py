from nvideos_web.services.base.error import ServiceException

class SubscriberChannelDoesntExists(ServiceException):
    pass

class SubscriberNoCurrentUser(ServiceException):
    pass

class SubscriberDoesntExists(ServiceException):
    pass