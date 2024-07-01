from dataclasses import dataclass

@dataclass
class Video:
    id: int
    title: str
    priv_or_pub: bool
    creator_user_id: int
