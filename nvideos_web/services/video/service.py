# FLASK
from locale import currency

from flask import current_app as app

# REDIS
from nvideos_web.db.redis import nredis

# TYPING
from typing import Self, override, final, cast, TypeAlias

# ENTITY
from nvideos_web.core.entity.video import (
    VideoInput, AuditData, Video, VideosRecommended,
    VideosHome
)

# CONSTANTS
from nvideos_web.core.entity.base.constants import VideoPermissions, VideoStatus

# SERVICES
from nvideos_web.services.base.service import BaseService

# ERROR
from nvideos_web.services.video.error import (
    VideoServiceNoVideoInput, VideoServiceVideoPermissionIsInvalid,
    VideoServiceChannelIdIsNone, VideoServiceVideoKeyIsNone,
    VideoServiceFailedToMoveTempVideoAndThumb, VideoServiceNoUserInput,
    VideoServiceVideoTitleIsNone, VideoServiceVideoTitleIsInvalid,
    VideoServiceVideoDescriptionIsInvalid, VideoServiceVideoDescriptionIsNone,
    VideoServiceVideoTagsIsInvalid, VideoServiceVideoTagsIsNone,
    VideoServiceVideoDoesntExists,
    VideoServiceChannelNameIsNone, VideoServiceMessageIsNone
)
from nvideos_web.services.base.error import InputDataIsNone

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# REPOSITORY
from nvideos_web.impl.video_repository import PgVideoRepository

VideoJson: TypeAlias = dict[str, object]
ListVideoJson: TypeAlias = list[VideoJson]

@final
class VideoService(BaseService[VideoInput]):
    def __init__(
        self, 
        *,
        userId: int | None = None,
        channelId: int | None = None,
        dbContext: type[NewVideosDBContext] | None = None
    ) -> None:
        super().__init__(currentUser=userId)
        #mypy doesn't understand inline if
        if dbContext is None:
            dbContext=NewVideosDBContext
        
        self._channelId: int | None = channelId

        self._videoRep: PgVideoRepository = PgVideoRepository(dbContext=dbContext)

        self._videoKey: str | None = None
        self._videoPermission: str | None = None

        self._videoThumbnailUrl: str | None = None
        self._videoTempFilename: str | None = None
        self._videoStatus: str | None = None

        #Redis
        self._enqueuedMessages: dict[str, list[dict[str, object]]] = {}

    def generateCheckVideoKey(self) -> Self:
        import hashlib, datetime
        if not self._channelId:
            raise VideoServiceChannelIdIsNone("The channel service is missing channel id.")
        
        randomData: str = datetime.datetime.now().isoformat() + str(self._channelId)
        
        while True:
            self._videoKey = hashlib.md5(randomData.encode("utf-8")).hexdigest()[:11]
            if not self._videoRep.checkKeyExists(self._videoKey):
                return self

    def moveTempFilesToNewPath(self, *, 
        videoThumbnailTempFilename: str | None, 
        videoTempFilename: str | None,
        channelId: int | None = None
    ) -> Self:
        # I'm maintaining this request because is a simple task, is not CPU bound, it's just a MOVE.
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        from typing import cast
        import json

        if not channelId and not self._channelId:
            raise VideoServiceChannelIdIsNone("The channel service is missing channel id.")
        elif self._channelId:
            channelId = self._channelId

        if not self._videoKey:
            raise VideoServiceVideoKeyIsNone("The video key is None.")

        req: Request = Request(
            url=f"{app.config['DOMAIN_MEDIA_SERVER']}/video/move/file/temp/{self._videoKey}/{videoTempFilename}/{videoThumbnailTempFilename}", 
            method="POST"
        )
        try:
            with urlopen(req) as response:
                bResponse: bytes = cast(bytes, response.read())
                jResponse: dict[str, str] = json.loads(bResponse.decode("utf-8"))
                
                videoTempFilename: str | None = jResponse.get("videofilename")
                videoThumbnailFilename: str | None = jResponse.get("thumbnailfilename")

                if not videoTempFilename:
                    raise VideoServiceFailedToMoveTempVideoAndThumb("Mediserver didn't return the video filename.")
                
                if not videoThumbnailFilename:
                    raise VideoServiceFailedToMoveTempVideoAndThumb("Mediserver didn't return the thumbnail filename.")
                
                self._videoThumbnailUrl = cast(str, app.config["DOMAIN_MEDIA_SERVER"]) + videoThumbnailFilename
                self._videoTempFilename = videoTempFilename
                self._videoStatus = VideoStatus.P_PROCESSING.value

                _ = self.enqueueMessageToChannelRedis(
                    channelName="video_upload",
                    message={
                        "videoKey": self._videoKey,
                        "videoFilename": self._videoTempFilename
                    }
                )

                return self
        except HTTPError:
            #add logger
            #_: bytes = e.read()
            raise VideoServiceFailedToMoveTempVideoAndThumb("The media server couldn't move the temp video and thumbnail to media.")

    def moveTempThumbToVideoPath(self, videoKey: str, videoThumbnailTempFilename: str) -> Self:
        # I'm maintaining this request because is a simple task, is not CPU bound, it's just a MOVE.
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        from typing import cast
        import json

        req: Request = Request(
            url=f"{app.config['DOMAIN_MEDIA_SERVER']}/video/move/thumb/temp/{videoKey}/{videoThumbnailTempFilename}", 
            method="POST"
        )
        try:
            with urlopen(req) as response:
                bResponse: bytes = cast(bytes, response.read())
                jResponse: dict[str, str] = json.loads(bResponse.decode("utf-8"))

                videoThumbnailFilename = jResponse.get("thumbnailfilename")

                if not videoThumbnailFilename:
                    # LOGGING: Add logger
                    raise VideoServiceFailedToMoveTempVideoAndThumb("Mediserver didn't return the thumbnail filename.")

                self._videoThumbnailUrl = cast(str, app.config["DOMAIN_MEDIA_SERVER"]) + videoThumbnailFilename
                return self
        except HTTPError:
            #LOGGING: Add logger
            #_: bytes = e.read()
            raise VideoServiceFailedToMoveTempVideoAndThumb("The media server couldn't move the temp thumbnail to media.")

    def translateVideoPermission(self, videoPermission: str | None) -> Self:
        options: list[str] = ["P", "S", "U", "R"]

        if videoPermission not in options:
            raise VideoServiceVideoPermissionIsInvalid("Video permission is invalid.")
        
        if videoPermission == "P":
            self._videoPermission = VideoPermissions.P_PUBLIC.value
        elif videoPermission == "S":
            self._videoPermission = VideoPermissions.P_SUBSCRIBER_ONLY.value
        elif videoPermission == "U":
            self._videoPermission = VideoPermissions.P_LINK_ONLY.value
        elif videoPermission == "R":
            self._videoPermission = VideoPermissions.P_PRIVATE.value

        return self

    def translateHtmlVideoPermission(self, videoPermission: str) -> str:
        if videoPermission == VideoPermissions.P_PUBLIC.value:
            return "P"
        elif videoPermission == VideoPermissions.P_SUBSCRIBER_ONLY.value:
            return "S"
        elif videoPermission == VideoPermissions.P_LINK_ONLY.value:
            return "U"
        elif videoPermission == VideoPermissions.P_PRIVATE.value:
            return "R"
        else:
            raise VideoServiceVideoPermissionIsInvalid("Video permission is invalid.")

    def checkVideoProcessingStatus(self, videoKey: str) -> str:
        redis: Redis = Redis.from_url(app.config["REDIS_ADDRESS"])
        percentReturn: bytes = cast(bytes, redis.get(f"video:processing:{videoKey}"))
        return percentReturn.decode("utf-8") if percentReturn else ""

    def finishedVideoProcessing(self, videoKey: str, timeDuration: int):
        inputData: VideoInput = self.fillInputData(
            videoStatus=VideoStatus.P_PROCESSED.value,
            videoTimeDuration=timeDuration
        ).getInputData()
        auditData: AuditData = self.fillAuditData(updatedBy=1).getAuditData()
        
        try:
            _ = self._videoRep.updateStatusByVideoKey(videoKey, inputData, auditData)
        except Exception:
            #log the error
            return

        return

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        self._checkExists: bool = self._videoRep.checkIdExists(videoId=idRegistry)
        return self

    def selectByVideoKey(self, videoKey: str) -> Video | None:
        videoData = self._videoRep.selectByVideoKey(videoKey)
        return videoData

    def selectByVideoKeyAndRecommended(self, videoKey: str, channelsUserIsSubscribed: list[int], /) -> tuple[Video, list[VideosRecommended]]:
        video, videoRecommended = self._videoRep.selectVideoKeyByIdAndRecommended(videoKey)

        #Filtering what users can see
        videoRecommended = [
            i for i in videoRecommended if i.checkUserCanSee(channelsUserIsSubscribed)
        ]

        return video, videoRecommended

    def selectLimitVideosByChannelId(self, limit: int = 10, *, page: int = 0) -> tuple[list[dict[str, object]] | None, int]:
        offset: int = page * limit
        
        if not self._channelId:
            raise VideoServiceChannelIdIsNone("Channel id is missing. Please provide a channel id.")

        videos, totalRows = self._videoRep.selectLimitCountVideoByChannelId(
            limit=limit,
            channelId=self._channelId,
            offset=offset
        )

        return [i.toJson() for i in videos], totalRows

    def selectLimitProcessedVideosByChannelId(self, 
        limit: int = 10, *,
        page: int = 0,
        userIsSubscribedToChannel: bool = False,
        userOwnVideoChannel: bool = False
    ) -> tuple[ListVideoJson | None, int]:
        offset: int = page * limit
        videoPermissions: list[str] | None = [
            VideoPermissions.P_PUBLIC.value,
        ] if not userOwnVideoChannel else None

        if userIsSubscribedToChannel and videoPermissions is not None:
            videoPermissions.append(VideoPermissions.P_SUBSCRIBER_ONLY.value)

        if not self._channelId:
            raise VideoServiceChannelIdIsNone("Channel id is missing. Please provide a channel id.")

        #Maybe I should do another service method just for channel videos
        #If anything changes I will add a new method to cover this part.
        videos, totalRows = self._videoRep.selectLimitCountVideoByChannelId(
            limit=limit,
            channelId=self._channelId,
            videoPermissions=videoPermissions,
            offset=offset, filterByStatus=VideoStatus.P_PROCESSED.value
        )

        #Since I will use this method to async pagination I will keep the return as "json"/dict.
        #So the view will mount with jinja2 using .get (dict) instead of ".property"
        return [i.toJson() for i in videos], totalRows

    def selectHomeVideos(self, filter: str, page: int, /, *, limit: int = 10): 
        limit: int = limit
        page: int = page
        offset: int = page * limit

        subscribedVideos: list[VideosHome] = []
        hasMoreSub = False

        if self.currentUser:
            limit = int(limit / 2)
            offset = page * limit

            subscribedVideos, hasMoreSub = self._videoRep.selectLastSubcribedVideos(filter, self.currentUser, limit=limit, offset=offset)
        
        publicVideos, hasMorePublic = self._videoRep.selectLastPublicVideos(filter, limit=limit, offset=offset)
        
        return subscribedVideos + publicVideos, hasMoreSub or hasMorePublic

    def increaseVideoViewCount(self, videoKey: str, /) -> Self:
        try:
            self._videoRep.incrementVideoViewCount(videoKey)
        except Exception as e:
            #LOG THE ERROR
            raise e

        return self

    def createNewVideo(self, *, userInput: VideoInput | None = None) -> Video:
        self.insertingMode()
        auditData = self.fillAuditData().getAuditData()
        userInput = userInput if userInput is not None else self._filledInputData

        if not userInput:
            raise VideoServiceNoVideoInput("No video input. Verify if you are setting the video input.")

        if userInput.videoStatus is None:
            userInput.videoStatus=VideoStatus.P_UPLOAD.value

        try:
            return self._videoRep.create(
                videoInputData=userInput, 
                auditInputData=auditData
            )
        finally:
            self.resetData()

    def updateVideoById(self, videoId: int, updatedByUserId: int | None = None) -> Video:
        self.updatingMode()
        auditData = self.fillAuditData(
            updatedBy=self.currentUser if self.currentUser else updatedByUserId
        ).getAuditData()
        inputData = self.getInputData()

        try:
            if not self.checkIdExists(idRegistry=videoId).getCheckIdExists():
                raise VideoServiceVideoDoesntExists("The user you trying to update doesn't exists")

            return self._videoRep.updateById(
                videoId=videoId,
                auditData=auditData,
                newVideoData=inputData
            )
        finally:
            self.resetData()

    def deleteVideoById(self, videoId: int, updatedByUserId: int | None = None) -> Video:
        self.updatingMode()
        auditData = self.fillAuditData(
            updatedBy=self.currentUser if self.currentUser else updatedByUserId
        ).getAuditData()

        try:
            if not self.checkIdExists(idRegistry=videoId).getCheckIdExists():
                raise VideoServiceVideoDoesntExists("The user you trying to update doesn't exists")

            return self._videoRep.delete(videoId, auditData)
        finally:
            self.resetData()

    def checkInputDataIsValid(self) -> Self:
        if not self._filledInputData:
            raise VideoServiceNoUserInput("The input data is missing.")
        
        if self._filledInputData.videoTitle is None:
            raise VideoServiceVideoTitleIsNone("The video title is missing.")
        elif len(self._filledInputData.videoTitle) <= 3:
            raise VideoServiceVideoTitleIsInvalid("The video title has less than 4 characters.")

        if self._filledInputData.videoDescription is None:
            raise VideoServiceVideoDescriptionIsNone("The video description is missing.")
        elif len(self._filledInputData.videoDescription) < 20:
            raise VideoServiceVideoDescriptionIsInvalid("The video description has less than 20 characters.")

        if self._filledInputData.videoTags is None:
            raise VideoServiceVideoTagsIsNone("The video tags is missing.")
        elif len(self._filledInputData.videoTags) < 2:
            raise VideoServiceVideoTagsIsInvalid("The video must have at least 1 tag.")

        return self

    @override
    def getInputData(self) -> VideoInput:
        if self._filledInputData is None:
            raise InputDataIsNone(InputDataIsNone.genericError())
        return self._filledInputData

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
        videoIsActive: bool | None = True,
        videoStatus: str | None = None,
        videoTempFilename: str | None = None
    ) -> Self:
        
        if self._videoPermission:
            videoPermission=self._videoPermission
            self._videoPermission=None

        if self.currentUser:
            userId = self.currentUser

        if self._channelId:
            channelId = self._channelId

        if self._videoThumbnailUrl:
            videoThumbUrl=self._videoThumbnailUrl
            self._videoThumbnailUrl=None

        if self._videoTempFilename:
            videoTempFilename=self._videoTempFilename
            self._videoTempFilename=None

        if self._videoKey:
            videoKey=self._videoKey
            self._videoKey=None

        if self._videoStatus:
            videoStatus=self._videoStatus
            self._videoStatus=None

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
            videoIsActive=videoIsActive,
            videoStatus=videoStatus,
            videoTempFilename=videoTempFilename
        )

        return self
    
    def fillCleanInputData(self, 
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
        videoIsActive: bool | None = True,
        videoStatus: str | None = None
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
            videoKey=videoKey,
            videoIsActive=videoIsActive,
            videoStatus=videoStatus
        )

        return self

    
    #Redis stuff - Maybe it will be part of baseService or a separeted module
    def enqueueMessageToChannelRedis(self, channelName: str, message: dict[str, object]) -> Self:
        if not channelName:
            raise VideoServiceChannelNameIsNone("Channel name is missing.")
        if not message:
            raise VideoServiceMessageIsNone("Message is missing.")

        if not self._enqueuedMessages.get(channelName):
            self._enqueuedMessages[channelName] = []

        self._enqueuedMessages[channelName].append(message)

        return self

    def processEnqueuedMessagesRedis(self):
        import json
        redis = nredis.client
        
        for channelName, messageList in self._enqueuedMessages.items():
            for message in messageList:
                _ = redis.publish(channelName.encode("utf-8"), json.dumps(message).encode("utf-8"))