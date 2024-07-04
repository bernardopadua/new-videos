from datetime import datetime
from dataclasses import dataclass, field, fields
from typing import (
    Type, TypeVar, Generic, 
    Callable, Optional, Any,
    cast
)
from mypy_extensions import DefaultNamedArg

#METADATA class
TMetadata = TypeVar("TMetadata", bound="MetadataClass")

#Model from METADATA class
TModel = TypeVar("TModel")

class ModelField:
    def __init__(
        self,
        fieldName: str, /, *, 
        attrName: str = "",
        owner: Type["MetadataClass"] | "MetadataClass" | None = None,
        isInstance: bool = False
    ) -> None:
        self.field: str = fieldName
        self.attr: str = attrName
        self.isInstance: bool = isInstance
        self.owner: Type["MetadataClass"] | "MetadataClass" | None = owner

    def getWithPrefix(self) -> str:
        if self.getOwner() is None:
            raise Exception("Owner of ModelField is none and it cannot be.")
        prefix: str = self.getOwner()._use_prefix
        return f"{prefix}.{self.field}"

    def getOwner(self) -> Type["MetadataClass"] | "MetadataClass":
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

TMethodSelf = TypeVar("TMethodSelf", bound="GetRowClassAndInstance")
class GetRowClassAndInstance(Generic[TMetadata, TModel]):
    def __init__(
        self: TMethodSelf, 
        method: Callable[[TMetadata, Any], TModel]
    ) -> None:
        self._method: Callable[[TMetadata, Any], TModel] = method

    def __get__(
        self: TMethodSelf, 
        instance: Optional["MetadataClass"], 
        classCaller: Type["MetadataClass"]
    ) -> Callable[[Any], TModel]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)
TGetModelData = TypeVar("TGetModelData", bound="GetModelData")
class GetModelData(Generic[TMetadata, TModel]):
    def __init__(
        self: TGetModelData, 
        method: Callable[[TMetadata], Type[TModel]]
    ) -> None:
       self._method: Callable[[TMetadata], Type[TModel]] = method

    def __get__(
        self: TGetModelData, 
        instance: Optional["MetadataClass"], 
        classCaller: Type["MetadataClass"]
    ) -> Callable[[], Type[TModel]]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)
TGetTableName = TypeVar("TGetTableName", bound="GetTableName")
class GetTableName(Generic[TMetadata]):
    def __init__(
        self: TGetTableName, 
        method: Callable[[TMetadata], str]
    ) -> None:
       self._method: Callable[[TMetadata], str] = method

    def __get__(
        self: TGetTableName, 
        instance: Optional["MetadataClass"], 
        classCaller: Type["MetadataClass"]
    ) -> Callable[[], str]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)
TGetTableNamePrefix = TypeVar("TGetTableNamePrefix", bound="GetTableNamePrefix")
class GetTableNamePrefix(Generic[TMetadata]):
    def __init__(
        self: TGetTableNamePrefix, 
        method: Callable[[TMetadata], str]
    ) -> None:
       self._method: Callable[[TMetadata], str] = method

    def __get__(
        self: TGetTableNamePrefix, 
        instance: Optional["MetadataClass"], 
        classCaller: Type["MetadataClass"]
    ) -> Callable[[], str]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)

class MetadataClass(Generic[TModel]):
    _table_name: str
    _model_data: Type[TModel] | None
    _use_prefix: str

    _all_fields: list[ModelField | ModelFieldKeyWord] = []

    all: ModelFieldKeyWord = ModelFieldKeyWord("*")

    def __init_subclass__(cls: Type[TMetadata], **kwargs) -> None:
        attrsCheck = ["_use_prefix", "_model_data", "_table_name"]
        if any(attr not in cls.__dict__ for attr in attrsCheck):
            raise Exception(f"Class {cls} metadata not implemented on of three main attributes.")

        super().__init_subclass__(**kwargs)
        def updateField(
            cls: Type[TMetadata], 
            attr: ModelField | ModelFieldKeyWord
        ):
            attr.attr = k
            attr.owner = cls

        for k in cls.__dict__:
            attr = cls.__dict__[k]
            if isinstance(attr, ModelField):
                cls._all_fields.append(attr)
                updateField(cls, attr)

        #__init_subclass__ doesnt include audit fields, so this step is necessary.
        #until I find a better way to do it. This will do it.
        auditFields = [i.__dict__ for i in cls.__mro__ if i is BaseMetadataAuditMixin]
        if len(auditFields) > 0:
            for k in auditFields[0]:
                attr = auditFields[0][k]
                if isinstance(attr, ModelField):
                    cls._all_fields.append(attr)
                    updateField(cls, attr)
        #'all' field doesn't is initialized too. So here we are adding one more step.
        allField = [i.__dict__ for i in cls.__mro__ if i is MetadataClass]
        if len(allField) > 0:
            attrAll: ModelFieldKeyWord = cast(ModelFieldKeyWord, allField[0].get('all'))
            #cls._all_fields.append(attrAll)
            updateField(cls, attrAll)

    def __init__(self: TMetadata, *, newPrefix: str) -> None:
        super().__init__()
        if not newPrefix:
            raise Exception("For a new instace of a table you need to inform a new prefix!")
        
        self._all_fields = []
        self._use_prefix = newPrefix

        for i in self.__dir__():
            attr = getattr(self, i)
            if isinstance(attr, ModelField):
                _m = ModelField(attr.field, attrName=attr.attr, owner=self, isInstance=True)
                setattr(self, i, _m)
                self._all_fields.append(_m)
            if isinstance(attr, ModelFieldKeyWord):
                _m = ModelFieldKeyWord(attr.field, attrName=attr.attr, owner=self, isInstance=True)
                setattr(self, i, _m)

    @GetTableNamePrefix
    def tableNamePrefix(clsSelf) -> str:
        return f"{clsSelf._table_name} {clsSelf._use_prefix}"

    @GetTableName["MetadataClass[TModel]"]
    def tableName(clsSelf) -> str:
        return clsSelf._table_name

    @classmethod
    def as_(cls: Type[TMetadata], *, newPrefix: str) -> TMetadata:
        return cls(newPrefix=newPrefix)

    @GetModelData["MetadataClass[TModel]", TModel]
    def modelData(
        clsSelf
    ) -> Type[TModel]:
        if clsSelf._model_data is None:
            raise Exception("Model cannot be null at the time of this call. If this is null, something wen wrong.")
        return clsSelf._model_data

    @GetRowClassAndInstance["MetadataClass[TModel]", TModel]
    def row(
        clsSelf, 
        rowDict: Any | None
    ) -> TModel:
        if rowDict is None:
            raise Exception("Rerturned row cannot be None.")
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
        print(self)

@dataclass
class BaseInput:
    def isNone(self) -> bool:
        isNone: bool = True
        for k in fields(self):
            if getattr(self, k.name) is not None:
                isNone = False
                break
        return isNone