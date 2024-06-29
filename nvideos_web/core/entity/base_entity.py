from datetime import datetime
from dataclasses import dataclass
from typing import Type, TypeVar

#METADATA class
T = TypeVar("T")

#Model from METADATA class
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

class BaseMetadataAuditMixin:
    updatedBy:ModelField = ModelField("updated_by")
    createdBy:ModelField = ModelField("created_by")
    createdAt:ModelField = ModelField("created_at")
    updatedAt:ModelField = ModelField("updated_at")
    all = "*"

class BaseMetadataUtilMixin:
    __table_name__: str = None
    __model_data__: M = None
    __use_prefix__: str = None

    # This typing was made to facilitate autocompletion rather than 
    # correctability of what type __model_data__ represents.
    @classmethod
    def model(cls: Type[M]) -> M:
        return cls.__model_data__
    @classmethod
    def get(cls: Type[M], row: dict[Type[M], M]) -> M:
        return row.get(cls.__model_data__)

@dataclass(frozen=True)
class AuditData:
    updatedBy: int
    createdBy: int
    createdAt: datetime
    updatedAt: datetime
