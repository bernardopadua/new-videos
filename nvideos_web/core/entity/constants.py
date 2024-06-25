from enum import Enum

class UserPermissions(Enum):
    P_SYSTEM = 0x0
    P_COMMOM_USER = 0x1

class VideoPermissions(Enum):
    P_PUBLIC = 0x0
    P_PRIVATE = 0x1
    P_SUBSCRIBER_ONLY = 0x2
    P_LINK_ONLY = 0x3
