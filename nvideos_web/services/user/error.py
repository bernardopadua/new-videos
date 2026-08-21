from nvideos_web.services.base.error import ServiceException

class UserServiceNoUserInput(ServiceException):
    """When trying to do something that needs user input and none was informed."""
    pass

class UserServiceUserDoesntExists(ServiceException):
    """When trying to do something that needs user and he wasn't informed."""
    pass

class UserServiceIncorrectUserEmailOrPassword(ServiceException):
    """Incorrect user email or password."""
    pass

## INPUT

class UserServiceUserDontMatchPassword(ServiceException):
    """When the informed password doesn't match the user's password."""
    pass

class UserServiceUserHasInvalidPassword(ServiceException):
    """Password has invalid characters."""
    pass

class UserServiceUserNameTooShort(ServiceException):
    """User name is too short."""
    pass

class UserServiceUserHasInvalidEmail(ServiceException):
    """Email has invalid characters."""
    pass

class UserServiceDateIsInvalid(ServiceException):
    """Date is invalid."""
    pass

class UserServiceUserHasInvalidPermission(ServiceException):
    """User has invalid permission."""
    pass

class UserServiceFailedToMoveTempAvatarToMedia(ServiceException):
    """Failed to move temp avatar to media."""
    pass

class UserServiceUserHasInvalidBirthDate(ServiceException):
    """User has invalid birth date."""
    pass