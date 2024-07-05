from typing import Protocol
from abc import abstractmethod

from nvideos_web.core.entity.channel import (
    Channel, ChannelInput
)

from nvideos_web.core.entity.base.base_entity import AuditData

class ChannelRepository(Protocol):
    @abstractmethod
    def create(self, channelInputData: ChannelInput, auditInputData: AuditData) -> Channel: 
        ...
    @abstractmethod
    def updateById(self, channelId: int, newChannelData: ChannelInput, auditData: AuditData) -> Channel: 
        ...
    @abstractmethod
    def delete(self, channelId: int, auditData: AuditData) -> Channel: 
        ...
