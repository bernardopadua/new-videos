from nvideos_web.services.base.error import ServiceException
# INIT
class UserCacheUserIdCannotBeNone(ServiceException):
    pass

# SERVICE METHODS
class UserCacheLoginSubscribedChannelsRedisSetError(ServiceException):
    pass

class UserCacheErrorDeletingChannelsSubscribed(ServiceException):
    pass
