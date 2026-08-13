# FLASK
from flask import current_app as app

# TYPING
from typing import Self
from typing_extensions import override, final

# SERVICES
from nvideos_web.services.base.service import BaseService

# ENTITY
from nvideos_web.core.entity.channel import Channel, ChannelInput, ChannelTotalSubscribers

# REPOSITORY
from nvideos_web.impl.channel_repository import PgChannelRepository

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# ERROR
from nvideos_web.services.base.error import InputDataIsNone
from nvideos_web.services.channel.error import (
    ChannelServiceCurrentUserIsNone, ChannelServiceChannelDoesntExists,
    ChannelServiceNameIsInvalid, ChannelServiceChannelDescriptionIsInvalid,
    ChannelServiceFailedToMoveTempImageToMedia, ChannelServiceNoCurrentUser
)

@final
class ChannelService(BaseService[ChannelInput]):
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

        self._chRep: PgChannelRepository = PgChannelRepository(dbContext=dbContext)
        self._avatarImageUrl: str | None = None
        self._coverImageUrl: str | None = None

    def selectChannelById(self, channelId: int, /) -> Channel | None:
        #I'm keeping it simple for now, will implement the other selects later
        try:
            channel = self._chRep.selectById(channelId=channelId)
            return channel
        except:
            return None
    
    def selectChannelByIdWithTotalSubscribers(self, channelId: int, /) -> tuple[Channel | None, ChannelTotalSubscribers | None]:
        #I'm keeping it simple for now, will implement the other selects later
        try:
            channel, totalSubscribers = self._chRep.selectByIdWithTotalSubscribers(channelId=channelId)
            return channel, totalSubscribers
        except:
            return None, None

    def checkInputDataIsValid(self, /) -> Self:
        _inputData = self.getInputData()
        
        if _inputData.channelName is None or len(_inputData.channelName) < 3:
            raise ChannelServiceNameIsInvalid("The informed channel name is invalid or is lower than 3 chars.")
        
        if _inputData.channelDescription is None or len(_inputData.channelDescription) > 1000:
            raise ChannelServiceChannelDescriptionIsInvalid("The informed channel description is invalid or is higher than 1000 chars.")

        return self

    def createNewChannel(self, /, *, inputData: ChannelInput | None = None) -> Channel:
        self.insertingMode()
        inputData = self.getInputData()
        auditData = self.fillAuditData().getAuditData()

        if inputData.userId is None and self._currentUser is None:
            raise ChannelServiceCurrentUserIsNone("Cannot insert None in the userId.")
        inputData.userId = inputData.userId if inputData.userId is not None else self._currentUser

        try:
            return self._chRep.create(channelInputData=inputData, auditInputData=auditData)
        finally:
            self.resetData()

    def updateChannelById(self, idRegistry: int, /, *, inputData: ChannelInput | None = None) -> Channel:
        _inputData = self.getInputData() if inputData is None else inputData
        _auditData = self.fillAuditData().getAuditData()

        try:
            if not self.checkIdExists(idRegistry=idRegistry).getCheckIdExists():
                raise ChannelServiceChannelDoesntExists("The channel you are trying to update doesn't exists.")

            return self._chRep.updateById(channelId=idRegistry, newChannelData=_inputData, auditData=_auditData)
        finally:
            self.resetData()

    def deleteChannelById(self, idRegistry: int, /) -> bool:
        _auditData = self.fillAuditData().getAuditData()

        try:
            if not self.checkIdExists(idRegistry=idRegistry).getCheckIdExists():
                raise ChannelServiceChannelDoesntExists("The channel you are trying to delete doesn't exists.")

            return self._chRep.deleteById(idRegistry=idRegistry, auditData=_auditData)
        finally:
            self.resetData()

    def hardDeleteChannelById(self, channelId: int, /) -> bool:
        try:
            return self._chRep.hardDelete(channelId=channelId)
        except:
            return False

    def doIAlreadyHaveChannel(self, /) -> Channel | None:
        if not self.currentUser:
            raise ChannelServiceNoCurrentUser("No current user informed.")

        return self._chRep.selectMyChannel(self.currentUser)

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        self._checkExists = self._chRep.checkIdExists(channelId=idRegistry)
        return self

    @override
    def getInputData(self) -> ChannelInput:
        if self._filledInputData is None:
            raise InputDataIsNone(InputDataIsNone.genericError())
        return self._filledInputData

    @override
    def fillInputData(
        self,
        /, *,
        channelName: str | None = None,
        channelDescription: str | None = None,
        channelImageUrl: str | None = None,
        channelAvatarUrl: str | None = None,
        channelIsActive: bool = True,
        userId: int | None = None
    ) -> Self:
        
        if self._avatarImageUrl:
            channelAvatarUrl = self._avatarImageUrl
            self._avatarImageUrl = None

        if self._coverImageUrl:
            channelImageUrl = self._coverImageUrl
            self._coverImageUrl = None

        self._filledInputData = ChannelInput(
            channelName=channelName,
            channelDescription=channelDescription,
            channelImageUrl=channelImageUrl,
            channelAvatarUrl=channelAvatarUrl,
            channelIsActive=channelIsActive,
            userId=userId
        )

        return self

    def moveTempImagesToMedia(self, channelId: int, avatarTempName: str | None = None, coverTempName: str | None = None) -> Self:
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        from typing import cast
        import json

        if avatarTempName:
            req: Request = Request(
                url=f"{app.config['DOMAIN_MEDIA_SERVER']}/channel/{channelId}/move/image/avatar/{avatarTempName}", 
                method="POST"
            )
            try:
                with urlopen(req) as response:
                    bResponse: bytes = cast(bytes, response.read())
                    jResponse: dict[str, str] = json.loads(bResponse.decode("utf-8"))
                    self._avatarImageUrl = app.config['DOMAIN_MEDIA_SERVER']+jResponse.get("imageUrl")
            except HTTPError as e:
                #add logger
                #_: bytes = e.read()
                raise ChannelServiceFailedToMoveTempImageToMedia("The media server couldn't move the temp avatar image to media.")
        if coverTempName:
            req: Request = Request(
                url=f"{app.config['DOMAIN_MEDIA_SERVER']}/channel/{channelId}/move/image/cover/{coverTempName}", 
                method="POST"
            )
            try:
                with urlopen(req) as response:
                    bResponse: bytes = cast(bytes, response.read())
                    jResponse: dict[str, str] = json.loads(bResponse.decode("utf-8"))
                    self._coverImageUrl = app.config['DOMAIN_MEDIA_SERVER']+jResponse.get("imageUrl")
            except HTTPError as e:
                #add logger
                #_: bytes = e.read()
                raise ChannelServiceFailedToMoveTempImageToMedia("The media server couldn't move the temp cover image to media.")

        return self
