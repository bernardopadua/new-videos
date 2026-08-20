# TYPING
from typing import Self, override, final, TypeAlias

# SERVICES
from nvideos_web.services.base.service import BaseService
from nvideos_web.services.user.service import UserService

# ENTITY
from nvideos_web.core.entity.subscriber import Subscriber, SubscriberInput
from nvideos_web.core.entity.user_subscriber import UserSubscriber

# REPOSITORY
from nvideos_web.impl.subscriber_repository import PgSubscriberRepository
from nvideos_web.impl.channel_repository import PgChannelRepository

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# ERRORS
from nvideos_web.services.base.error import InputDataIsNone
from nvideos_web.services.subscriber.error import (
    SubscriberChannelDoesntExists, SubscriberNoCurrentUser,
    SubscriberDoesntExists
)

ChannelSubscribed: TypeAlias = dict[str, int | str]
ChannelSubscribedList: TypeAlias = list[ChannelSubscribed]

@final
class SubscriberService(BaseService[SubscriberInput]):
    def __init__(
        self, 
        *,
        userId: int | None = None, 
        dbContext: type[NewVideosDBContext] | None = None
    ) -> None:
        super().__init__(currentUser=userId)
        #mypy doesn't understand inline if
        if dbContext is None:
            dbContext=NewVideosDBContext

        self._usuRep: PgSubscriberRepository = PgSubscriberRepository(dbContext=dbContext)
        self._chRep: PgChannelRepository = PgChannelRepository(dbContext=dbContext)

    def subscribeToChannel(self, channelId: int) -> UserSubscriber | None:
        if not self.currentUser:
            raise SubscriberNoCurrentUser("No current user informed.")
        if not self._chRep.checkIdExists(channelId=channelId):
            raise SubscriberChannelDoesntExists("Channel that the user is trying to subscribe doesn't exists.")

        subscriber = self._usuRep.selectByChannelIdAndUserId(channelId, self.currentUser)
        if subscriber and not subscriber.subscriberIsActive:
            self.updatingMode()
            auditData = self.fillAuditData().getAuditData()
            inputData = self.fillInputData(subscriberIsActive=True).getInputData()
            
            try:
                user = UserService(userId=self.currentUser).selectByUserId()
                subscriber = self._usuRep.updateById(subscriber.subscriberId, inputData, auditData)
                return UserSubscriber(
                    user=user,
                    subscriber=subscriber
                )
            finally:
                self.resetData()
            
        elif subscriber is None:
            self.insertingMode()
            auditData = self.fillAuditData().getAuditData()
            inputData = self._filledInputData if self._filledInputData else self.fillInputData(
                channelId=channelId,
                userId=self._currentUser,
                subscriberIsActive=True
            ).getInputData()

            try:
                return self._usuRep.create(subscriberInputData=inputData, auditInputData=auditData)
            finally:
                self.resetData()
        
        return None

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        pass
        return self

    def checkSubscribedAndSubscribe(self, channelId: int) -> UserSubscriber | None:
        if self.currentUser is None:
            raise SubscriberNoCurrentUser("No current user informed.")

        isSubscribed: bool = self._usuRep.checkAlreadySubscribed(channelId, self.currentUser)
        if not isSubscribed:
            return self.subscribeToChannel(channelId)

        return None

    def checkSubscribedAndUnsubscribe(self, channelId: int) -> bool:
        if self.currentUser is None:
            raise SubscriberNoCurrentUser("No current user informed.")
        
        subscriber: Subscriber | None = self._usuRep.selectByChannelIdAndUserId(channelId, self.currentUser)
        if subscriber is None:
            raise SubscriberDoesntExists("Subscriber not found.")

        self.updatingMode()
        auditData = self.fillAuditData().getAuditData()
        
        try:
            subscriber = self._usuRep.delete(subscriber.subscriberId, auditData)
            if not subscriber.subscriberIsActive:
                return True
            
            return False
        except Exception:
            #LOG: add logging
            return False
        finally:
            self.resetData()

    def checkAlreadySubscribed(self, channelId: int) -> bool:
        if self.currentUser is None:
            raise SubscriberNoCurrentUser("No current user informed.")

        return self._usuRep.checkAlreadySubscribed(channelId, self.currentUser)

    def selectTotalSubscribers(self, channelId: int) -> int:
        return self._usuRep.selectTotalSubscribers(channelId)

    def selectChannelsIdsUserIsSubscribed(self, /, *, userId: int | None = None) -> list[int]:
        if self.currentUser:
            userId = self.currentUser
        elif userId is None:
            raise SubscriberNoCurrentUser("No current user informed.")

        return self._usuRep.selectChannelsIdsUserIsSubscribed(userId)

    def selectChannelsUserIsSubscribed(self, /) -> list[dict[str, int | str]] | None:
        if self.currentUser is None:
            raise Exception("No current user informed.")
        
        try:
            chs = self._usuRep.selectChannelsUserIsSubscribed(self.currentUser)

            if chs is None:
                return None

            return [{
                "channelId": ch.channelId,
                "channelName": ch.channelName,
                "channelAvatarUrl": ch.channelAvatarUrl
            } for ch in chs]
        except Exception:
            return None
        
    @override
    def getInputData(self) -> SubscriberInput:
        if self._filledInputData is None:
            raise InputDataIsNone(InputDataIsNone.genericError())

        return self._filledInputData

    @override
    def fillInputData(
        self, /, *,
        channelId: int | None = None,
        userId: int | None = None,
        subscriberIsActive: bool | None = None
    ) -> Self:

        self._filledInputData = SubscriberInput(
            channelId=channelId,
            userId=userId,
            subscriberIsActive=subscriberIsActive
        )

        return self