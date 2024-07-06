# TYPING
from typing import Any, Type

# SERVICES
from nvideos_web.services.base.service import BaseService

# ENTITY
from nvideos_web.core.entity.channel import Channel, ChannelInput

# REPOSITORY
from nvideos_web.impl.channel_repository import PgChannelRepository

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# ERROR
from nvideos_web.services.base.error import InputDataIsNone
from nvideos_web.services.channel.error import ChannelServiceCurrentUserIsNone, ChannelServiceChannelDoesntExists

class ChannelService(BaseService["ChannelService", ChannelInput]):
    def __init__(
        self, 
        *,
        userId: int | None = None, 
        dbContext: Type[NewVideosDBContext] | None = None
    ) -> None:
        super().__init__(currentUser=userId)
        #mypy doesn't understand inline if
        if dbContext is None:
            dbContext=NewVideosDBContext

        self._chRep = PgChannelRepository(dbContext=dbContext)

    def createNewChannel(self, /, *, inputData: ChannelInput | None = None) -> Channel:
        self.insertingMode()
        inputData = self.getInputData()
        auditData = self.fillAuditData().getAuditData()

        if inputData.userId is None and self._currentUser is None:
            ChannelServiceCurrentUserIsNone("Cannot insert None in the userId.")
        inputData.userId = inputData.userId if inputData.userId is not None else self._currentUser

        try:
            return self._chRep.create(channelInputData=inputData, auditInputData=auditData)
        finally:
            self.resetData()

    def checkIdExists(self, channelId: int) -> "ChannelService":
        self._checkExists = self._chRep.checkIdExists(channelId=channelId)
        return self

    def updateChannelById(self, channelId: int, /, *, inputData: ChannelInput | None = None) -> Channel:
        _inputData = self.getInputData() if inputData is None else inputData
        _auditData = self.fillAuditData().getAuditData()

        try:
            if not self.checkIdExists(channelId=channelId).getCheckIdExists():
                raise ChannelServiceChannelDoesntExists("The channel you are trying to update doesn't exists.")

            return self._chRep.updateById(channelId=channelId, newChannelData=_inputData, auditData=_auditData)
        finally:
            self.resetData()

    def getInputData(self) -> ChannelInput:
        if self._filledInputData is None:
            raise InputDataIsNone(InputDataIsNone.genericError())
        return self._filledInputData

    def fillInputData(
        self,
        /, *,
        channelName: str | None = None,
        channelDescription: str | None = None,
        channelImageUrl: str | None = None,
        channelAvatarUrl: str | None = None,
        userId: int | None = None
    ) -> "ChannelService":
        
        self._filledInputData = ChannelInput(
            channelName=channelName,
            channelDescription=channelDescription,
            channelImageUrl=channelImageUrl,
            channelAvatarUrl=channelAvatarUrl,
            userId=userId
        )

        return self
