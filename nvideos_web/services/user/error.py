class UserServiceNoUserInput(Exception):
    """When trying to do something that needs user input and none was informed."""
    pass

class UserServiceUserDoesntExists(Exception):
    """When trying to do something that needs user and he wasn't informed."""
    pass

class UserServiceUserDontMatchPassword(Exception):
    """When the informed password doesn't match the user's password."""
    pass

class UserServiceUserHasInvalidPassword(Exception):
    """Password has invalid characters."""
    pass

class UserServiceUserNameTooShort(Exception):
    """User name is too short."""
    pass

class UserServiceUserHasInvalidEmail(Exception):
    """Email has invalid characters."""
    pass

class UserServiceDateIsInvalid(Exception):
    """Date is invalid."""
    pass

class UserServiceUserHasInvalidPermission(Exception):
    """User has invalid permission."""
    pass

class UserServiceFailedToMoveTempAvatarToMedia(Exception):
    """Failed to move temp avatar to media."""
    pass

class UserServiceUserHasInvalidBirthDate(Exception):
    """User has invalid birth date."""
    pass