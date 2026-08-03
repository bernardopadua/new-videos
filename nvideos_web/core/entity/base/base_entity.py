from __future__ import annotations

# BUILT-IN
from datetime import datetime
from dataclasses import dataclass, field, fields

# TYPING
from typing import (
    TypeVar, Generic, 
    Callable, Any, cast
)

AVOID_PREFIX_REPETITION: list[str] = []

#METADATA class
TMetadata = TypeVar("TMetadata", bound="MetadataClass[object]")

#Model from METADATA class
TModel = TypeVar("TModel")

class ModelField:
    def __init__(
        self,
        fieldName: str, /, *, 
        attrName: str = "",
        owner: type[MetadataClass[object]] | None = None,
        isInstance: bool = False
    ) -> None:
        self.field: str = fieldName
        self.attr: str = attrName
        self.isInstance: bool = isInstance
        self.owner: type[MetadataClass[object]] | None = owner

    def getWithPrefix(self) -> str:
        prefix: str = self.getOwner().getPrefix()
        return f"{prefix}.{self.field}"

    def getOwner(self) -> type[MetadataClass[object]]:
        if self.owner is None:
            raise Exception("Owner cannot be None at this step. Investigate.")
        return self.owner

class ModelFieldKeyWord(ModelField):
    pass

class GetRowClassAndInstance(Generic[TModel]):
    def __init__(
        self, 
        method: Callable[[MetadataClass[TModel], dict[int, TModel]], TModel]
    ) -> None:
        self._method: Callable[[MetadataClass[TModel], dict[int, TModel]], TModel] = method

    def __get__(
        self, 
        instance: MetadataClass[TModel] | None, 
        classCaller: type[MetadataClass[TModel]]
    ) -> Callable[[object], TModel]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)

class GetModelData(Generic[TModel]):
    def __init__(
        self, 
        method: Callable[[MetadataClass[TModel]], type[TModel]]
    ) -> None:
       self._method: Callable[[MetadataClass[TModel]], type[TModel]] = method

    def __get__(
        self, 
        instance: MetadataClass[TModel] | None, 
        classCaller: type[MetadataClass[TModel]]
    ) -> Callable[[], type[TModel]]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)

class GetTableName(Generic[TModel]):
    def __init__(
        self, 
        method: Callable[[MetadataClass[TModel]], str | None]
    ) -> None:
       self._method: Callable[[MetadataClass[TModel]], str | None] = method

    def __get__(
        self, 
        instance: MetadataClass[TModel] | None, 
        classCaller: type[MetadataClass[TModel]]
    ) -> Callable[[], str]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)

class GetTableNamePrefix(Generic[TMetadata]):
    def __init__(
        self, 
        method: Callable[[TMetadata], str]
    ) -> None:
       self._method: Callable[[TMetadata], str] = method

    def __get__(
        self, 
        instance: MetadataClass[TModel] | None, 
        classCaller: type["MetadataClass[TModel]"]
    ) -> Callable[[], str]:
        if instance is None:
            return self._method.__get__(classCaller, classCaller)
        return self._method.__get__(instance, classCaller)

class MetadataClass(Generic[TModel]):
    _table_name: str | None = None
    _model_data: type[TModel] | None = None
    _use_prefix: str

    _all_fields: list[ModelField | ModelFieldKeyWord]

    all: ModelFieldKeyWord | None = None

    def __init_subclass__(cls: type[TMetadata], **kwargs: object) -> None:
        attrsCheck = ["_use_prefix", "_model_data", "_table_name"]
        if any(attr not in cls.__dict__ for attr in attrsCheck):
            raise Exception(f"Class {cls} metadata not implemented on of three main attributes.")

        super().__init_subclass__(**kwargs)

        #Initializing a new list
        cls.all = ModelFieldKeyWord("*", attrName="all", owner=cls)
        cls._all_fields = []

        if cls._use_prefix in AVOID_PREFIX_REPETITION:
            raise Exception(f"Prefix used by {cls} class it is already taken. Please try to use another one.")
        AVOID_PREFIX_REPETITION.append(cls._use_prefix)

        for k in cls.__dict__:
            attr: ModelField | ModelFieldKeyWord | Any = cls.__dict__[k]
            isKeyword: bool = isinstance(attr, ModelFieldKeyWord)
            if isinstance(attr, ModelField) and not isKeyword:
                attr.attr = k
                attr.owner = cls
                cls._all_fields.append(attr)

        #__init_subclass__ doesnt include audit fields, so this step is necessary.
        #until I find a better way to do it. This will do it.
        auditFields = [i.__dict__ for i in cls.__mro__ if i is BaseMetadataAuditMixin]
        if len(auditFields) > 0:
            for k in auditFields[0]:
                #attr = auditFields[0][k]
                try:
                    attr = getattr(cls, k)
                except Exception:
                    continue
                if isinstance(attr, ModelField):
                    attr = ModelField(attr.field, attrName=k, owner=cls)
                    setattr(cls, k, attr)
                    cls._all_fields.append(attr)

    def __init__(self, *, newPrefix: str) -> None:
        super().__init__()
        if not newPrefix:
            raise Exception("For a new instace of a table you need to inform a new prefix!")
        
        self._all_fields = []
        self._use_prefix = newPrefix

        for i in self.__dir__():
            attr = getattr(self, i)
            if isinstance(attr, ModelField):
                #TODO: I must solve this cast, it's horrible... rethink all this entity thing
                _m = ModelField(attr.field, attrName=attr.attr, 
                    owner=cast(type[MetadataClass[object]], self), isInstance=True
                )
                setattr(self, i, _m)
                self._all_fields.append(_m)
            if isinstance(attr, ModelFieldKeyWord):
                _m = ModelFieldKeyWord(attr.field, attrName=attr.attr, 
                    owner=cast(type[MetadataClass[object]], self), isInstance=True
                )
                setattr(self, i, _m)
    
    @classmethod
    def getPrefix(cls) -> str:
        return cls._use_prefix

    @GetTableNamePrefix
    def tableNamePrefix(clsSelf) -> str:
        return f"{clsSelf._table_name} {clsSelf._use_prefix}"

    @GetTableName[TModel]
    def tableName(clsSelf) -> str | None:
        return clsSelf._table_name

    @classmethod
    def as_(cls: type[TMetadata], *, newPrefix: str) -> TMetadata:
        return cls(newPrefix=newPrefix)

    @GetModelData[TModel]
    def modelData(
        clsSelf
    ) -> type[TModel]:
        if clsSelf._model_data is None:
            raise Exception("Model cannot be null at the time of this call. If this is null, something went wrong.")
        return clsSelf._model_data

    @GetRowClassAndInstance[TModel]
    def row(
        clsSelf, 
        rowDict: dict[int, TModel] | None
    ) -> TModel:
        if rowDict is None:
            raise Exception("Rerturned row cannot be None.")
        return rowDict[id(clsSelf)]

#class BaseMetadataAuditMixin(Generic[TMetadata]):
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