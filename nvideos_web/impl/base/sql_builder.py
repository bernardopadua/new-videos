# PSYCOPG
from psycopg import _queries

# BUILT-IN
from dataclasses import is_dataclass

# TYPING
from typing import TypeVar, Type

# BASE ENTITY
from nvideos_web.core.entity.base_entity import ModelField, ModelFieldKeyWord

# IMPL
from nvideos_web.impl.error.base import (
    PgRepositoryInputIsNotDataclass,
    PgRepositoryMissingSqlParameter
)

GenericInputClass = TypeVar("GenericInputClass")

class NvSql:
    def __init__(self: "NvSql", *, usePrefix: bool = False) -> None:
        self._sql: str = ""
                
        self._fieldsListOrder: list[ModelField] = []
        self._tables: list[str]

        self._usePrefix: bool = usePrefix

    def selectFields(self: "NvSql", *args: ModelField | ModelFieldKeyWord) -> "NvSql":
        if len(args) == 1 and args[0].field == "*":
            for attr in args[0].owner.__dict__:
                if isinstance(attr, ModelField):
                    self._fieldsListOrder.append(attr)
        for arg in args:
            if isinstance(arg, ModelFieldKeyWord) and arg.field == "*":
                self.selectFields(arg)
            self._fieldsListOrder.append(arg)

        if len(self._fieldsListOrder) <= 0:
            raise Exception("Fields must be passed to continue to generate a valid SQL.")
        
        return self

    def select(self: "NvSql", *args: ModelField | ModelFieldKeyWord) -> "NvSql":
        self._isSelecting = True
        self.selectFields(*args)
        return self

    def insert(self: "NvSql", *args: ModelField | ModelFieldKeyWord) -> "NvSql":
        self._isInserting = True
        self.selectFields(*args)
        self._insertTable = self._fieldsListOrder[0].getOwner()._table_name
        return self

    def build(self: "NvSql") -> None:
        pass

    @staticmethod
    def literal(*args):
        concat = []
        for i in args:
            concat.append(i)
        return ''.join(concat)

    @staticmethod
    def selectOder(
        *args: ModelField | ModelFieldKeyWord
    ) -> tuple[str, list[ModelField]]:
        concat = []
        listRowFactory = []
        for arg in args:
            concat.append(arg.field)
            listRowFactory.append(arg)
        return (','.join(concat), listRowFactory)

    @staticmethod
    def parseSqlParams(
        _sql: str, 
        inputObject: GenericInputClass,
        *,
        auditObject: GenericInputClass | None = None
    ) -> dict:
        if not is_dataclass(inputObject):
            raise PgRepositoryInputIsNotDataclass(
                "Object passed to parsing params is not dataclass."
            )

        paramAssigned = {}
        sqlParams = _queries._re_placeholder.finditer(
            bytes(_sql.encode('utf-8'))
        )
        for param in sqlParams:
            inputFieldValue = None
            paramAttr = _sql[param.span(0)[0]+2:param.span(0)[1]-2]
            
            try:
                if not hasattr(inputObject, paramAttr) and auditObject:
                    inputFieldValue = getattr(auditObject, paramAttr)
                else:
                    inputFieldValue = getattr(inputObject, paramAttr)
            except AttributeError as e:
                raise PgRepositoryMissingSqlParameter(
                    "Parameter has no input field. Please verify the input and audit objects."
                )

            paramAssigned[paramAttr] = inputFieldValue

        return paramAssigned

    #TODO: use metadata to assign the values from select