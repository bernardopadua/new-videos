from datetime import datetime
from dataclasses import dataclass
from typing import Type, TypeVar

T = TypeVar("T")
M = TypeVar("M")

def modelMetadataMapper(cls: Type[T]) -> T:
    props = cls.__dict__
    for k in props:
        if isinstance(props[k], ModelField):
            p: ModelField = props[k]
            p.attr = k
            p.owner = cls
    return cls

class ModelField:
    def __init__(self, fieldName: str, /, *, attrName: str = "") -> None:
        self.field:str = fieldName
        self.attr:str = attrName
        self.owner:object = None

class BaseMetadata:
    updatedBy:ModelField = ModelField("updated_by")
    createdBy:ModelField = ModelField("created_by")
    createdAt:ModelField = ModelField("created_at")
    updatedAt:ModelField = ModelField("updated_at")
    all = "*"

    @classmethod
    def model(cls: Type[M]) -> M:
        return cls.__model_data__

@dataclass(frozen=True)
class AuditData:
    updatedBy: int
    createdBy: int
    createdAt: datetime
    updatedAt: datetime
