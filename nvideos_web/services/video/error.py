from nvideos_web.services.base.error import ServiceException

class VideoServiceUserNotAuthenticated(ServiceException):
    """The user is not authenticated."""
    pass

class VideoServiceVideoDoesntExists(ServiceException):
    """The video doesn't exists."""
    pass

class VideoServiceNoVideoInput(ServiceException):
    """No video input provided. Please provide video input."""
    pass

class VideoServiceVideoPermissionIsInvalid(ServiceException):
    """The informed video permission is invalid."""
    pass

class VideoServiceChannelIdIsNone(ServiceException):
    """The channel service is missing channel id."""
    pass

class VideoServiceVideoKeyIsNone(ServiceException):
    """The video key is None."""
    pass

class VideoServiceFailedToMoveTempVideoAndThumb(ServiceException):
    """The video and thumbnail files were not moved from temp to the media server."""
    pass

# CHECK FOR INVALID FIELDS
class VideoServiceNoUserInput(ServiceException):
    """No user input provided. Please provide user input."""
    pass

class VideoServiceVideoTitleIsNone(ServiceException):
    """The video title is None."""
    pass

class VideoServiceVideoTitleIsInvalid(ServiceException):
    """The video title is invalid."""
    pass

class VideoServiceVideoDescriptionIsNone(ServiceException):
    """The video description is None."""
    pass

class VideoServiceVideoDescriptionIsInvalid(ServiceException):
    """The video description is invalid."""
    pass

class VideoServiceVideoTagsIsNone(ServiceException):
    """The video tags is None."""
    pass

class VideoServiceVideoTagsIsInvalid(ServiceException):
    """The video tags is invalid."""
    pass

# REDIS ERRORS
class VideoServiceChannelNameIsNone(ServiceException):
    """The channel name is None."""
    pass

class VideoServiceMessageIsNone(ServiceException):
    """The message is None."""
    pass
