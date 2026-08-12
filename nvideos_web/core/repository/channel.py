# BUILT-IN
from abc import ABC, abstractmethod

# ENTITY
from nvideos_web.core.entity.channel import (
    Channel, ChannelInput, ChannelTotalSubscribers
)

from nvideos_web.core.entity.base.base_entity import AuditData

class ChannelRepository(ABC):
    @abstractmethod
    def selectMyChannel(self, userId: int) -> Channel | None:
        ...
    @abstractmethod
    def selectById(self, channelId: int) -> Channel | None:
        ...
    @abstractmethod
    def selectByIdWithTotalSubscribers(self, channelId: int) -> tuple[Channel | None, ChannelTotalSubscribers | None]:
        ...
    @abstractmethod
    def selectChannelsIdsUserIsSubscribed(self, userId: int) -> list[int]:
        ...
    @abstractmethod
    def create(self, channelInputData: ChannelInput, auditInputData: AuditData) -> Channel: 
        ...
    @abstractmethod
    def checkIdExists(self, channelId: int) -> bool: 
        ...
    @abstractmethod
    def updateById(self, channelId: int, newChannelData: ChannelInput, auditData: AuditData) -> Channel: 
        ...
    @abstractmethod
    def delete(self, channelId: int, auditData: AuditData) -> Channel: 
        ...
    @abstractmethod
    def hardDelete(self, channelId: int) -> bool: 
        ...