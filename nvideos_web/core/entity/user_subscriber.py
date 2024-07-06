# DATACLASS
from dataclasses import dataclass

# ENTITY
from nvideos_web.core.entity.user import User
from nvideos_web.core.entity.subscriber import Subscriber

@dataclass(frozen=True, slots=True)
class UserSubscriber:
    user: User
    subscriber: Subscriber