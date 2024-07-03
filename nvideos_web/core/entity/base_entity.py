from datetime import datetime
from dataclasses import dataclass, field
from typing import (
    Type, TypeVar, Generic, 
    Callable, Optional
)

#METADATA class
TMetada = TypeVar("TMetada", bound="MetadataClass")

#Model from METADATA class
TModel = TypeVar("TModel")

class ModelField(Generic[TMetada]):
    def __init__(
        self: "ModelField", 
        fieldName: str, /, *, 
        attrName: str = "",
        owner: Type[TMetada] | TMetada | None = None
    ) -> None:
        self.field: str = fieldName
        self.attr: str = attrName
        self.owner: Type[TMetada] | TMetada | None = owner

    def getWithPrefix(self: "ModelField") -> str:
        if self.owner is None:
            raise Exception("Owner of ModelField is none and it cannot be.")
        prefix: str = self.owner._use_prefix
        return f"{prefix}.{self.field}"

    def getOwner(self) -> Type[TMetada] | TMetada:
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

class MethodClassAndInstance(Generic[TModel]):
    def __init__(
        self: "MethodClassAndInstance", 
        method: Callable[[
            Type["MetadataClass"] | "MetadataClass",
            dict[int, TModel]
        ], TModel]
    ) -> None:
        self._method: Callable[[
            Type["MetadataClass"] | "MetadataClass",
            dict[int, TModel]], TModel] = method
    
    def __get__(
        self: "MethodClassAndInstance", 
        instance: Optional["MetadataClass"], 
        classCaller: Type["MetadataClass"]
    ) -> Callable[[dict[int, TModel]], TModel]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)

class MetadataClass(Generic[TModel]):
    _table_name: str
    _model_data: Type[TModel] | None
    _use_prefix: str

    all: ModelFieldKeyWord = ModelFieldKeyWord("*")

    def __init_subclass__(cls, **kwargs) -> None:
        attrsCheck = ["_use_prefix", "_model_data", "_table_name"]
        if any(attr not in cls.__dict__ for attr in attrsCheck):
            raise Exception(f"Class {cls} metadata not implemented on of three main attributes.")

        super().__init_subclass__(**kwargs)
        def updateField(
            cls: Type["MetadataClass"], 
            attr: ModelField | ModelFieldKeyWord
        ):
            attr.attr = k
            attr.owner = cls

        for k in cls.__dict__:
            attr = cls.__dict__[k]
            if isinstance(attr, ModelField) or isinstance(attr, ModelFieldKeyWord):
                updateField(cls, attr)

        #__init_subclass__ doesnt include audit fields, so this step is necessary.
        #until I find a better way to do it. There will do it.
        auditFields = [i.__dict__ for i in cls.__mro__ if i is BaseMetadataAuditMixin]
        if len(auditFields) > 0:
            for k in auditFields[0]:
                attr = auditFields[0][k]
                if isinstance(attr, ModelField) or isinstance(attr, ModelFieldKeyWord):
                    updateField(cls, attr)

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
    def tableName(cls: Type[TMetada]) -> str:
        return cls._table_name

    @classmethod
    def as_(cls: Type[TMetada], *, newPrefix: str) -> TMetada:
        return cls(newPrefix=newPrefix)

    @MethodClassAndInstance[TModel]
    def getRow(
        clsSelf: Type["MetadataClass"] | "MetadataClass", 
        rowDict: dict[int, TModel]
    ) -> TModel:
        return rowDict[id(clsSelf)]

class BaseMetadataAuditMixin:
    updatedBy: ModelField = ModelField("updated_by")
    createdBy: ModelField = ModelField("created_by")
    createdAt: ModelField = ModelField("created_at")
    updatedAt: ModelField = ModelField("updated_at")

@dataclass(frozen=True, slots=True)
class AuditData:
    updatedBy: int | None = field(default=None)
    createdBy: int | None = field(default=None)
    createdAt: datetime | None = field(default=None)
    updatedAt: datetime | None = field(default=None)

@dataclass(frozen=True, slots=True)
class BaseModelData:
    def print(self):
        pass