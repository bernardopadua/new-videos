# PSYCOPG
from psycopg import Connection

# BUILT-IN
from abc import ABC, abstractmethod

# ENTITY
from nvideos_web.core.entity.video import (
    Video,
    VideoInput
)
from nvideos_web.core.entity.base.base_entity import AuditData

class VideoRepository(ABC):
    @abstractmethod
    def create(self, videoInputData: VideoInput, auditInputData: AuditData) -> Video: 
        ...
    @abstractmethod
    def checkIdExists(self, videoId: int) -> bool: 
        ...
    @abstractmethod
    def checkKeyExists(self, videoKey: str) -> bool: 
        ...
    @abstractmethod
    def selectByVideoKey(self, videoKey: str, userId: int) -> Video: 
        ...
    @abstractmethod
    def selectLimitVideosByChannelId(self, limit: int, 
        channelId: int, *, offset: int = 0, 
        conn: Connection | None = None
    ) -> list[Video]:
        ...
    @abstractmethod
    def selectCountAllVideoByChannelId(self, channelId: int, *, conn: Connection | None = None) -> int: 
        ...
    @abstractmethod
    def selectLimitCountVideoByChannelId(self, *, limit: int, channelId: int, offset: int = 0) -> tuple[list[Video], int]:
        ...
    @abstractmethod
    def updateById(self, videoId: int, newVideoData: VideoInput, auditData: AuditData) -> Video: 
        ...
    @abstractmethod
    def updateStatusByVideoKey(self, videoKey: str, newVideoData: VideoInput, auditData: AuditData) -> Video: 
        ...
    @abstractmethod
    def delete(self, videoId: int, auditData: AuditData) -> Video: 
        ...
