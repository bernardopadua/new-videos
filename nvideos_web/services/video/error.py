class VideoServiceNoVideoInput(Exception):
    """No video input provided. Please provide video input."""
    pass

class VideoServiceVideoPermissionIsInvalid(Exception):
    """The informed video permission is invalid."""
    pass