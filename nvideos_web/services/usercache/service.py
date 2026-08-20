# TYPING
from typing import final

# DB / REDIS
from nvideos_web.db.redis import nredis

# ERROR
from nvideos_web.services.usercache.error import (
    UserCacheLoginSubscribedChannelsRedisSetError,
    UserCacheUserIdCannotBeNone
)

# CACHE KEYS
from nvideos_web.db.redis_constants import USER_SUBSCRIBED_CHANNELS_KEY

# BUILT-IN
import json

@final
class UserCacheService:
    def __init__(self, userId: int | None):
        if userId is None:
            #TODO: Logging
            raise UserCacheUserIdCannotBeNone("We having problems setting user information. Contact Support.")
        self._userId = userId

    def setLogin(self, /, *,
        channels: list[dict[str, str | int]] | None = None
    ):
        if channels is not None:
            self.setUserSubscribedChannels(channels)

    def setUserSubscribedChannels(self, channels: list[dict[str, str | int]]):
        """Set the subscribed channels of a user"""
        if nredis.client.set(
            USER_SUBSCRIBED_CHANNELS_KEY.format(userId=self._userId),
            json.dumps(channels)
        ) is None:
            #TODO: Logging
            raise UserCacheLoginSubscribedChannelsRedisSetError("We having problems setting user information. Contact Support.")
    
    def unsetUserSubscribedChannels(self):
        _ = nredis.client.delete(USER_SUBSCRIBED_CHANNELS_KEY.format(userId=self._userId))

    def clearCache(self):
        """Clear the cache of a user"""
        self.unsetUserSubscribedChannels()
            
