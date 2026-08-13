from nvideos_web.services.base.error import ServiceException

class ChannelServiceCurrentUserIsNone(ServiceException):
    pass

class ChannelServiceChannelDoesntExists(ServiceException):
    pass

class ChannelServiceNameIsInvalid(ServiceException):
    pass

class ChannelServiceChannelDescriptionIsInvalid(ServiceException):
    pass

class ChannelServiceFailedToMoveTempImageToMedia(ServiceException):
    pass

class ChannelServiceNoCurrentUser(ServiceException):
    """ No CurrentUser informed when created the service """
    pass
