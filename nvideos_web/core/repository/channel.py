# BUILT-IN
from abc import ABC, abstractmethod

# ENTITY
from nvideos_web.core.entity.channel import (
    Channel, ChannelInput
)

from nvideos_web.core.entity.base.base_entity import AuditData

class ChannelRepository(ABC):
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
