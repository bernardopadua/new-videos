from nvideos_web.impl.error.base import PgRepositoryException

class VideoIsNone(PgRepositoryException):
    """Some return or instance of Video is None in a context it cannot be."""
    pass