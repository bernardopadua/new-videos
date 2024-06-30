from datetime import datetime
from dataclasses import dataclass
from typing import Type, TypeVar, Any

#METADATA class
T = TypeVar("T")

#Model from METADATA class
M = TypeVar("M")

def modelMetadataMapper(cls: Type[T]) -> Type[T]:
    props = cls.__dict__
    for k in props:
        if isinstance(props[k], ModelField) or isinstance(props[k], ModelFieldKeyWord):
            p: ModelField = props[k]
            p.attr = k
            p.owner = cls
    return cls

class ModelField:
    def __init__(
        self: "ModelField", 
        fieldName: str, /, *, 
        attrName: str = "",
        owner: Type[T] | T = None
    ) -> None:
        self.field: str = fieldName
        self.attr: str = attrName
        self.owner: Type[T] | T = owner

    def getWithPrefix(self: "ModelField") -> str:
        prefix: str = self.owner.__use_prefix__
        return f"{prefix}.{self.field}"

    def __eq__(
        self: "ModelField", value: "ModelField",
        *, usePrefix: bool = False
    ) -> str:
        nField: str = self.field if not usePrefix else self.getWithPrefix()
        if not isinstance(value, ModelField):
            return f"{nField} = {value}"
        
        fieldComp: str = value.field if not usePrefix else value.getWithPrefix()
        return f"{nField} = {fieldComp}"

class ModelFieldKeyWord(ModelField):
    pass

class BaseMetadataAuditMixin:
    updatedBy: ModelField = ModelField("updated_by")
    createdBy: ModelField = ModelField("created_by")
    createdAt: ModelField = ModelField("created_at")
    updatedAt: ModelField = ModelField("updated_at")

class BaseMetadataUtilMixin:
    __table_name__: str = None
    __model_data__: M = None
    __use_prefix__: str = None

    all: ModelFieldKeyWord = ModelFieldKeyWord("*")

    def __init__(self: T, *, newPrefix: str = None):
        if not newPrefix:
            raise Exception("For a new instace of a table you need to inform a new prefix!")

        self.__use_prefix__ = newPrefix

        for i in self.__dir__():
            attr = getattr(self, i)
            if isinstance(attr, ModelField):
                setattr(self, i, ModelField(attr.field, attrName=attr.attr, owner=self))
            if isinstance(attr, ModelFieldKeyWord):
                setattr(self, i, ModelFieldKeyWord(attr.field, attrName=attr.attr, owner=self))
    
    def getTable(self: T) -> str:
        return self.__table_name__

    @classmethod
    def as_(cls: Type[T], newPrefix: str = None):
        return cls(newPrefix=newPrefix)

    @classmethod
    def getTable(cls: Type[T]) -> str:
        return cls.__table_name__

    @classmethod
    def model(cls: Type[T]) -> M:
        return cls.__model_data__

@dataclass(frozen=True)
class AuditData:
    updatedBy: int
    createdBy: int
    createdAt: datetime
    updatedAt: datetime

@dataclass(frozen=True, slots=True)
class BaseModelData:
    @classmethod
    def get(cls: Type[M], row: dict[Type[M], M]) -> M:
        return row.get(cls)