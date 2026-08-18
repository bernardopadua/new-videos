# PSYCOPG
from psycopg import _queries

# BUILT-IN
from dataclasses import is_dataclass, fields

# TYPING
from typing import LiteralString, TypeVar, Self, cast, TypeAlias

# BASE ENTITY
from nvideos_web.core.entity.base.base_entity import MetadataClass, ModelField, ModelFieldKeyWord

# IMPL
from nvideos_web.core.entity.user import UserInput
from nvideos_web.impl.error.base import (
    PgRepositoryInputIsNotDataclass,
    PgRepositoryMissingSqlParameter
)

TNvSqlModelField = TypeVar("TNvSqlModelField")
FieldsCommaStr: TypeAlias = str
ParamsCommaStr: TypeAlias = str

ParamPgSQL: TypeAlias = str
ParamPgMapObject: TypeAlias = dict[str, object]

class NvSql:
    def __init__(self, *, usePrefix: bool = False) -> None:
        self._sql: str = ""
                
        self._fieldsListOrder: list[ModelField] = []
        self._tables: list[str]

        self._usePrefix: bool = usePrefix

        self._isSelecting: bool = False
        self._isInserting: bool = False

        self._insertTable: str | None = ""

    def selectFields(self, *args: ModelField | ModelFieldKeyWord) -> Self:
        if len(args) == 1 and args[0].field == "*":
            for attr in args[0].owner.__dict__:
                if isinstance(attr, ModelField):
                    self._fieldsListOrder.append(attr)
        for arg in args:
            if isinstance(arg, ModelFieldKeyWord) and arg.field == "*":
                _ = self.selectFields(arg)
            self._fieldsListOrder.append(arg)

        if len(self._fieldsListOrder) <= 0:
            raise Exception("Fields must be passed to continue to generate a valid SQL.")
        
        return self

    def select(self, *args: ModelField | ModelFieldKeyWord) -> Self:
        self._isSelecting = True
        _ = self.selectFields(*args)
        return self

    def insert(self, *args: ModelField | ModelFieldKeyWord) -> Self:
        self._isInserting = True
        _ = self.selectFields(*args)
        self._insertTable = self._fieldsListOrder[0].getOwner().getTableName()
        return self

    #TODO: 2 years not messing with this project.
    # I just comment this for now to avoid problems with basedpyright
    # @staticmethod
    # def literal(*args):
    #     concat: list[str] = []
    #     for i in args:
    #         concat.append(i)
    #     return ''.join(concat)

    @staticmethod
    def createParam(paramName: str, paramValue: object) -> tuple[ParamPgSQL, ParamPgMapObject]:
        parsedParam: object = ""
        
        #I messed up.
        #if isinstance(paramValue, str):
        #    parsedParam = f"'{paramValue}'"
        #else:
        parsedParam = paramValue

        return f"%({paramName})s", {paramName: parsedParam}

    @staticmethod
    def concatParams(*args: ParamPgMapObject) -> ParamPgMapObject:
        concatParams: ParamPgMapObject = {}
        for i in args:
            concatParams = {**i, **concatParams}
        return concatParams

    @staticmethod
    def selectOder(
        *args: ModelField | ModelFieldKeyWord,
        usePrefix: bool = False,
        useAsinFields: bool = False
    ) -> tuple[FieldsCommaStr, list[ModelField]]:
        newArgs: list[ModelField | ModelFieldKeyWord] = [*args]
        concat: list[str] = []
        listRowFactory: list[ModelField] = []
        
        if len(newArgs) == 1 and isinstance(args[0], ModelFieldKeyWord) and \
        args[0].field == "*":
            attr: ModelFieldKeyWord = args[0]
            newArgs = attr.getOwner().getAllFields()

        for arg in newArgs:
            if usePrefix and useAsinFields:
                concat.append(f"{arg.getWithPrefix()} as \"{arg.attr}\"")
            elif usePrefix:
                concat.append(arg.getWithPrefix())
            elif useAsinFields:
                concat.append(f"{arg.field} as \"{arg.attr}\"")
            else:
                concat.append(arg.field)
            listRowFactory.append(arg)
        return (','.join(concat), listRowFactory)

    @staticmethod
    def selectOrderToFields(fieldsOrder: list[ModelField], /, *, usePrefix: bool = False) -> FieldsCommaStr:
        arFields:list[str] = []
        
        if usePrefix:
            for f in fieldsOrder:
                arFields.append(f.getWithPrefix())
        else:
            for f in fieldsOrder:
                arFields.append(f.field)

        return ','.join(arFields)

    @staticmethod
    def parseSqlParams(
        _sql: str, 
        inputObject: object,
        *,
        auditObject: object | None = None,
        additionalParams: dict[str, object] | None = None
    ) -> dict[str, object]:
        if not is_dataclass(inputObject):
            raise PgRepositoryInputIsNotDataclass(
                "Object passed to parsing params is not dataclass."
            )

        paramAssigned: dict[str, object] = {}
        #TODO: I need to create this on my own to avoid using psycpg modules.
        # For now I will use the psycpg module
        sqlParams = _queries._re_placeholder.finditer(
            bytes(_sql.encode('utf-8'))
        )
        for param in sqlParams:
            inputFieldValue: object | None = None
            paramAttr = _sql[param.span(0)[0]+2:param.span(0)[1]-2]
            
            try:
                if hasattr(inputObject, paramAttr):
                    inputFieldValue = getattr(inputObject, paramAttr)
                elif auditObject and hasattr(auditObject, paramAttr):
                    inputFieldValue = getattr(auditObject, paramAttr)
                elif additionalParams and paramAttr in additionalParams:
                    inputFieldValue = additionalParams[paramAttr]
            except AttributeError:
                raise PgRepositoryMissingSqlParameter(
                    "Parameter has no input field. Please verify the input and audit objects."
                )

            paramAssigned[paramAttr] = inputFieldValue

        return paramAssigned

    @staticmethod
    def formatStmt(_stmt: str, **kwargs: object) -> LiteralString:
        return cast(LiteralString, _stmt.format(**kwargs))

    @staticmethod
    def updateFields(_metaData: type[MetadataClass[TNvSqlModelField]], inputData: object) -> str:
        retMapValue: list[str] = []
        if not is_dataclass(inputData):
            raise Exception("Expecting a input of dataclass type.")

        for field in fields(inputData):
            fieldInput: object = getattr(inputData, field.name)
            if fieldInput is not None:
                try:
                    metadataAttr: ModelField = cast(ModelField, getattr(_metaData, field.name))
                    retMapValue.append(f"{metadataAttr.field} = %({field.name})s")
                except AttributeError:
                    continue
                except Exception as e:
                    raise e

        return ', '.join(retMapValue)

    @staticmethod
    def insertFieldsOrder(_metaData: type[MetadataClass[TNvSqlModelField]], inputData: object) -> tuple[FieldsCommaStr, ParamsCommaStr, list[ModelField]]:
        retFieds: list[str] = []
        retParams: list[str] = []
        retListOrder: list[ModelField] = []

        if not is_dataclass(inputData):
            raise Exception("Expecting a input of dataclass type.")

        for field in fields(inputData):
            fieldInput: object = getattr(inputData, field.name)
            if fieldInput is not None:
                try:
                    metadataAttr: ModelField = cast(ModelField, getattr(_metaData, field.name))
                    retFieds.append(f"{metadataAttr.field}")
                    retParams.append(f"%({field.name})s")
                    retListOrder.append(metadataAttr)
                except AttributeError:
                    continue
                except Exception as e:
                    raise e

        return (",".join(retFieds), ",".join(retParams), retListOrder)