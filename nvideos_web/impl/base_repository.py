# BUILT-IN
from typing import ( 
    Sequence, Any, Type,
    TypeVar
)
from dataclasses import is_dataclass

# PSYCOPG
from psycopg import _queries, Cursor
from psycopg.rows import RowMaker

# ENTITY
from nvideos_web.core.entity.base_entity import ModelField, ModelFieldKeyWord

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext

# IMPL
from nvideos_web.impl.error.base import (
    PgRepositoryInputIsNotDataclass,
    PgRepositoryMissingSqlParameter
)

GenericInputClass = TypeVar("GenericInputClass")
M = TypeVar("M")

#TODO: I'm gonna use this ?
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

    @classmethod
    def literal(*args):
        concat = []
        for i in args:
            concat.append(i)
        return ''.join(concat)

class ModelRowFactory(RowMaker):
    def __init__(
        self, 
        listOrderFields: list[ModelField],
        /, *,
        modelReturn: Type[M] | None = None
    ):
        self.fields = listOrderFields
        self.returningModel = modelReturn

    def __call__(
        self, 
        *args: Sequence[Any]
    ) -> dict[int, Any] | "ModelRowFactory":
    #RowMaker[dict[int, Any] | "ModelRowFactory"]:
        if len(args) == 0:
            raise Exception("RowFactory is been called with no parameters.")
        if len(args) > 0 and isinstance(args[0], Cursor):
            return self

        values: Sequence[Any] = args[0]
        eachModel: dict[int, dict[str, Any]] = {}
        instancesModel: dict[int, object] = {}
        
        #TODO: I dont know if I will be implementing this yet. 
        #The idea is to return a different value-object and assemble this special case object at this step.
        #retObject: M = None

        for i in range(len(values)):
            field: ModelField = self.fields[i]
            modelIdentification: int = id(field.owner)
            if modelIdentification not in eachModel:
                eachModel[modelIdentification] = { "model": field.getOwner()._model_data, "row": {} }
            eachModel[modelIdentification]["row"].update({ field.attr: values[i] })

        #TODO: I don't know if I want to continue this. I think the default is working OK, at least for now.
        # if self.returningModel:
        #     retObject = self.returningModel()

        #     for model in eachModel.keys():
        #         if not retObject.__dict__.get(model):
        #             raise Exception("Model assigned to return the query doesn't exists as a type of returned query.")

        #         for attr in retObject.__dict__.keys():
        #             if isinstance(retObject.__dict__[attr], model):
        #                 setattr(retObject, attr, model(**eachModel[model])) 
            
        #    instancesModel[self.returningModel] = retObject
        #    return instancesModel
        
        for model in eachModel.keys():
            modelData = eachModel[model]["model"]
            instancesModel[model] = modelData(**eachModel[model]["row"])

        return instancesModel

    @classmethod
    def getRowFactory(
        cls: Type["ModelRowFactory"], 
        listOrderFields: list[ModelField]
    ) -> "ModelRowFactory":
        return cls(listOrderFields)

class PgRepositoryBase:
    _dbContext: Type[NewVideosDBContext]

    def __init__(self, dbContext: Type[NewVideosDBContext]) -> None:
        self._dbContext = dbContext

    def sqlFields(self, *args: ModelField) -> tuple[str, list[ModelField]]:
        concat = []
        listRowFactory = []
        for arg in args:
            concat.append(arg.field)
            listRowFactory.append(arg)
        return (','.join(concat), listRowFactory)

    def parseSqlParams(
        self, _sql: str, 
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
                
                inputFieldValue = getattr(inputObject, paramAttr)
            except AttributeError as e:
                raise PgRepositoryMissingSqlParameter(
                    "Parameter has no input field. Please verify the input and audit objects."
                )

            paramAssigned[paramAttr] = inputFieldValue

        return paramAssigned

    #TODO: use metadata to assign the values from select