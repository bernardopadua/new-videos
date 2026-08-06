class ChannelServiceCurrentUserIsNone(Exception):
    pass

class ChannelServiceChannelDoesntExists(Exception):
    pass

class ChannelServiceNameIsInvalid(Exception):
    pass

class ChannelServiceChannelDescriptionIsInvalid(Exception):
    pass

class ChannelServiceFailedToMoveTempImageToMedia(Exception):
    pass

class ChannelServiceNoCurrentUser(Exception):
    """ No CurrentUser informed when created the service """
    pass
