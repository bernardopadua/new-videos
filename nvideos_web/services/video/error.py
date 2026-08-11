class VideoServiceUserNotAuthenticated(Exception):
    """The user is not authenticated."""
    pass

class VideoServiceVideoDoesntExists(Exception):
    """The video doesn't exists."""
    pass

class VideoServiceNoVideoInput(Exception):
    """No video input provided. Please provide video input."""
    pass

class VideoServiceVideoPermissionIsInvalid(Exception):
    """The informed video permission is invalid."""
    pass

class VideoServiceChannelIdIsNone(Exception):
    """The channel service is missing channel id."""
    pass

class VideoServiceVideoKeyIsNone(Exception):
    """The video key is None."""
    pass

class VideoServiceFailedToMoveTempVideoAndThumb(Exception):
    """The video and thumbnail files were not moved from temp to the media server."""
    pass

# CHECK FOR INVALID FIELDS
class VideoServiceNoUserInput(Exception):
    """No user input provided. Please provide user input."""
    pass

class VideoServiceVideoTitleIsNone(Exception):
    """The video title is None."""
    pass

class VideoServiceVideoTitleIsInvalid(Exception):
    """The video title is invalid."""
    pass

class VideoServiceVideoDescriptionIsNone(Exception):
    """The video description is None."""
    pass

class VideoServiceVideoDescriptionIsInvalid(Exception):
    """The video description is invalid."""
    pass

class VideoServiceVideoTagsIsNone(Exception):
    """The video tags is None."""
    pass

class VideoServiceVideoTagsIsInvalid(Exception):
    """The video tags is invalid."""
    pass

# REDIS ERRORS
class VideoServiceChannelNameIsNone(Exception):
    """The channel name is None."""
    pass

class VideoServiceMessageIsNone(Exception):
    """The message is None."""
    pass
