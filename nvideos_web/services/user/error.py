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
