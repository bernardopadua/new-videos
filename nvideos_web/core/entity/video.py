from dataclasses import dataclass
from nvideos_web.core.entity.entity_base import BaseFieldsMixin

@dataclass
class Video(BaseFieldsMixin):
    id: int
    title: str
    priv_or_pub: bool
    creator_user_id: int
