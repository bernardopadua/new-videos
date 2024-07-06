# BUILT-IN
from abc import abstractmethod

# TYPING
from typing import Protocol

# ENTITY
from nvideos_web.core.entity.subscriber import (
    Subscriber, SubscriberInput
)
from nvideos_web.core.entity.user_subscriber import UserSubscriber
from nvideos_web.core.entity.base.base_entity import AuditData

class SubscriberRepository(Protocol):
    @abstractmethod
    def create(self, subscriberInputData: SubscriberInput, auditInputData: AuditData) -> UserSubscriber:
        ...
    @abstractmethod
    def checkIdExists(self, subscriberId: int) -> bool:
        ...
    @abstractmethod
    def updateById(self, subscriberId: int, newSubscriberData: SubscriberInput, auditData: AuditData) -> Subscriber:
        ...
    @abstractmethod
    def delete(self, subscriberId: int, auditData: AuditData) -> Subscriber:
        ...
