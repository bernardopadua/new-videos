# TYPING
from typing import Self, override, final

# ENTITY
from nvideos_web.core.entity.video import VideoInput

# SERVICES
from nvideos_web.services.base.service import BaseService

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

    def generateCheckVideoKey(self, videoKey: str) -> str:
        ...

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        ...

    @override
    def getInputData(self) -> VideoInput:
        ...

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
        videoKey: str | None = None
    ) -> Self:
        
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
            videoKey=videoKey
        )

        return self
