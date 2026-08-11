# BUILT-IN
from abc import ABC, abstractmethod

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
    def updateById(self, videoId: int, newVideoData: VideoInput, auditData: AuditData) -> Video: 
        ...
    @abstractmethod
    def updateStatusByVideoKey(self, videoKey: str, newVideoData: VideoInput, auditData: AuditData) -> Video: 
        ...
    @abstractmethod
    def delete(self, videoId: int, auditData: AuditData) -> Video: 
        ...
