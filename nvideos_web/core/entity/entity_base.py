from datetime import datetime
from dataclasses import dataclass

def modelMetadataMapper(cls: object):
    props = cls.__dict__
    for k in props:
        if isinstance(props[k], ModelField):
            p: ModelField = props[k]
            p.attr = k
            p.owner = cls
    return cls

class ModelMetaMetaClass:
    def __new__(cls, a, b, c, *args, **kwargs):
        ncls = super().__new__(cls)

        return ncls

class ModelField:
    def __init__(self, fieldName: str, *, attrName: str = "") -> None:
        self.field:str = fieldName
        self.attr:str = attrName
        self.owner:object = None

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
