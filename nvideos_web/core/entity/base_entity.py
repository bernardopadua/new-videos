from datetime import datetime
from dataclasses import dataclass

def modelMetadataMapper(cls: object) -> None:
    props = cls.__dict__
    for k in props:
        if isinstance(props[k], ModelField):
            p: ModelField = props[k]
            p.attr = k
            p.owner = cls
    return cls

def mapToMetadata(cls: object, metadata: object) -> None:
    metadata.__model_class__ = cls
    return cls

class ModelField:
    def __init__(self, fieldName: str, *, attrName: str = "") -> None:
        self.field:str = fieldName
        self.attr:str = attrName
        self.owner:object = None

class BaseMetadata:
    updatedBy:ModelField = ModelField("updated_by")
    createdBy:ModelField = ModelField("created_by")
    createdAt:ModelField = ModelField("created_at")
    updatedAt:ModelField = ModelField("updated_at")
    all = "*"

@dataclass(frozen=True)
class AuditData:
    updatedBy: int
    createdBy: int
    createdAt: datetime
    updatedAt: datetime
