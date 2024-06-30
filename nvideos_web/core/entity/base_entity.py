from datetime import datetime
from dataclasses import dataclass
from typing import Type, TypeVar, Generic, Protocol

#METADATA class
T = TypeVar("T", bound="MetadataClass")

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

class MetadataClass(Protocol[M]):
    _table_name: str
    _model_data: Type[M]
    _use_prefix: str

    def __init_subclass__(cls) -> None:
        pass
        return super().__init_subclass__()

class ModelField(Generic[T]):
    def __init__(
        self: "ModelField", 
        fieldName: str, /, *, 
        attrName: str = "",
        owner: Type[T] | None = None
    ) -> None:
        self.field: str = fieldName
        self.attr: str = attrName
        self.owner: Type[T] | None = owner

    def getWithPrefix(self: "ModelField") -> str:
        prefix: str = self.owner._use_prefix
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

class BaseMetadataUtilMixin(Generic[M]):
    __table_name__: str
    __model_data__: Type[M]
    __use_prefix__: str

    all: ModelFieldKeyWord = ModelFieldKeyWord("*")

    def __init__(self, *, newPrefix: str = None):
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
    def as_(cls, newPrefix: str = None):
        return cls(newPrefix=newPrefix)

    @classmethod
    def getTable(cls) -> str:
        return cls.__table_name__

    @classmethod
    def model(cls) -> M:
        return cls.__model_data__

@dataclass(frozen=True)
class AuditData:
    updatedBy: int
    createdBy: int
    createdAt: datetime
    updatedAt: datetime
