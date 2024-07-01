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

class ModelField(Generic[T]):
    def __init__(
        self: "ModelField", 
        fieldName: str, /, *, 
        attrName: str = "",
        owner: Type[T] | T | None = None
    ) -> None:
        self.field: str = fieldName
        self.attr: str = attrName
        self.owner: Type[T] | T | None = owner

    def getWithPrefix(self: "ModelField") -> str:
        if self.owner is None:
            raise Exception("Owner of ModelField is none and it cannot be.")
        prefix: str = self.owner._use_prefix
        return f"{prefix}.{self.field}"

    def getOwner(self) -> Type[T] | T:
        if not self.owner:
            raise Exception("Owner cannot be None at this step. Investigate.")
        return self.owner

    # def __eq__(
    #     self: "ModelField", value: "ModelField",
    #     *, usePrefix: bool = False
    # ) -> str:
    #     nField: str = self.field if not usePrefix else self.getWithPrefix()
    #     if not isinstance(value, ModelField):
    #         return f"{nField} = {value}"
        
    #     fieldComp: str = value.field if not usePrefix else value.getWithPrefix()
    #     return f"{nField} = {fieldComp}"

class ModelFieldKeyWord(ModelField):
    pass

class MetadataClass(Generic[M]):
    _table_name: str
    _model_data: Type[M] | None
    _use_prefix: str

    all: ModelFieldKeyWord = ModelFieldKeyWord("*")

    def __init_subclass__(cls, **kwargs) -> None:
        attrsCheck = ["_use_prefix", "_model_data", "_table_name"]
        if any(attr not in cls.__dict__ for attr in attrsCheck):
            raise Exception(f"Class {cls} metadata not implemented on of three main attributes.")

        super().__init_subclass__(**kwargs)
        for k in cls.__dict__:
            attr = cls.__dict__[k]
            if isinstance(attr, ModelField) or isinstance(attr, ModelFieldKeyWord):
                attr.attr = k
                attr.owner = cls

    def __del__(cls):
        pass

    def __init__(self, *, newPrefix: str) -> None:
        super().__init__()
        if not newPrefix:
            raise Exception("For a new instace of a table you need to inform a new prefix!")

        self._use_prefix = newPrefix

        for i in self.__dir__():
            attr = getattr(self, i)
            if isinstance(attr, ModelField):
                setattr(self, i, ModelField(attr.field, attrName=attr.attr, owner=self))
            if isinstance(attr, ModelFieldKeyWord):
                setattr(self, i, ModelFieldKeyWord(attr.field, attrName=attr.attr, owner=self))

    @classmethod
    def as_(cls: Type["MetadataClass"], *, newPrefix: str) -> "MetadataClass":
        return cls(newPrefix=newPrefix)

class BaseMetadataAuditMixin:
    updatedBy: ModelField = ModelField("updated_by")
    createdBy: ModelField = ModelField("created_by")
    createdAt: ModelField = ModelField("created_at")
    updatedAt: ModelField = ModelField("updated_at")

@dataclass(frozen=True)
class AuditData:
    updatedBy: int
    createdBy: int | None
    createdAt: datetime | None
    updatedAt: datetime
