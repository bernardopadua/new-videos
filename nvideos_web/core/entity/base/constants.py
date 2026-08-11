from enum import Enum

class UserPermissions(Enum):
    P_SYSTEM = '\x01'
    P_COMMOM_USER = '\x02'

class VideoPermissions(Enum):
    P_PUBLIC = '\x01'
    P_PRIVATE = '\x02'
    P_SUBSCRIBER_ONLY = '\x03'
    P_LINK_ONLY = '\x04'

class VideoStatus(Enum):
    P_UPLOAD = 'uploaded'
    P_PROCESSING = 'processing'
    P_PROCESSED = 'processed'