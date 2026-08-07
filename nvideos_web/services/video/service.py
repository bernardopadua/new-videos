# TYPING
from typing import Self, override, final, cast

# ENTITY
from nvideos_web.core.entity.video import VideoInput, Video

# CONSTANTS
from nvideos_web.core.entity.base.constants import UserPermissions

# SERVICES
from nvideos_web.services.base.service import BaseService

# ERROR
from nvideos_web.services.video.error import (
    VideoServiceNoVideoInput, VideoServiceVideoPermissionIsInvalid
)

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# REPOSITORY
from nvideos_web.impl.video_repository import PgVideoRepository

@final
class VideoService(BaseService[VideoInput]):
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
            
        self._videoRep: PgVideoRepository = PgVideoRepository(dbContext=dbContext)

        self._videoKey: str | None = None
        self._videoPermission: str | None = None

    def generateCheckVideoKey(self, videoKey: str) -> str:
        ...

    def translateVideoPermission(self, videoPermission: str | None) -> Self:
        options: list[str] = ["P", "S", "U", "R"]

        if videoPermission not in options:
            raise VideoServiceVideoPermissionIsInvalid("Video permission is invalid.")
        
        if videoPermission == "P":
            self._videoPermission = cast(str, UserPermissions.P_PUBLIC.value)
        elif videoPermission == "S":
            self._videoPermission = cast(str, UserPermissions.P_SUBSCRIBER.value)
        elif videoPermission == "U":
            self._videoPermission = cast(str, UserPermissions.P_UNLISTED.value)
        elif videoPermission == "R":
            self._videoPermission = cast(str, UserPermissions.P_PRIVATE.value)

        return self

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        ...

    @override
    def getInputData(self) -> VideoInput:
        ...

    def createNewVideo(self, *, userInput: VideoInput | None = None) -> Video:
        self.insertingMode()
        auditData = self.fillAuditData().getAuditData()
        userInput = userInput if userInput else self._filledInputData

        if not userInput:
            raise VideoServiceNoVideoInput("No video input. Verify if you are setting the video input.")

        try:
            return self._videoRep.create(
                videoInputData=userInput, 
                auditInputData=auditData
            )
        finally:
            self.resetData()

    @override
    def fillInputData(self, 
        /, *,
        videoTitle: str | None = None,
        videoDescription: str | None = None,
        videoTimeDuration: int | None = None,
        videoViewCount: int | None = None,
        videoThumbUrl: str | None = None,
        videoTags: list[str] | None = None,
        videoPermission: str | None = None,
        channelId: int | None = None,
        userId: int | None = None,
        videoKey: str | None = None,
        videoIsActive: bool | None = True
    ) -> Self:
        
        if self._videoPermission:
            videoPermission=self._videoPermission
            self._videoPermission=None

        if self.currentUser:
            userId = self.currentUser

        self._filledInputData = VideoInput(
            videoTitle=videoTitle,
            videoDescription=videoDescription,
            videoTimeDuration=videoTimeDuration,
            videoViewCount=videoViewCount,
            videoThumbUrl=videoThumbUrl,
            videoTags=videoTags,
            videoPermission=videoPermission,
            channelId=channelId,
            userId=userId,
            videoKey=videoKey,
            videoIsActive=videoIsActive
        )

        return self
