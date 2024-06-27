from datetime import datetime
from dataclasses import dataclass

class ModelField:
    def __init__(self, *, attrName: str, fieldName: str) -> None:
        self.field:str = fieldName
        self.attr:str = attrName

class BaseMetadata:
    updatedBy = "updated_by"
    createdBy = "created_by"
    createdAt = "created_at"
    updatedAt = "updated_at"
    all = "*"

@dataclass(frozen=True)
class AuditData:
    updatedBy: int
    createdBy: int
    createdAt: datetime
    updatedAt: datetime
