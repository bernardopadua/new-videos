# TYPING
from typing import Self, override, final

# SERVICES
from nvideos_web.services.base.service import BaseService

# ENTITY
from nvideos_web.core.entity.subscriber import SubscriberInput
from nvideos_web.core.entity.user_subscriber import UserSubscriber

# REPOSITORY
from nvideos_web.impl.subscriber_repository import PgSubscriberRepository
from nvideos_web.impl.channel_repository import PgChannelRepository

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# ERRORS
from nvideos_web.services.base.error import InputDataIsNone
from nvideos_web.services.subscriber.error import SubscriberChannelDoesntExists

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

    def subscribeToChannel(self, channelId: int) -> UserSubscriber:
        if not self._chRep.checkIdExists(channelId=channelId):
            raise SubscriberChannelDoesntExists("Channel that the user is trying to subscribe doesn't exists.")
        
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

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        raise NotImplementedError()
        return super().checkIdExists(idRegistry)

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