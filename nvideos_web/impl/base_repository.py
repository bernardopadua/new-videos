# BUILT-IN
from typing import ( 
    Sequence, Any, Type,
    TypeVar, Optional
)
from dataclasses import is_dataclass

# PSYCOPG
from psycopg import _queries, Cursor

# ENTITY
from nvideos_web.core.entity.base_entity import ModelField

# IMPL
from nvideos_web.impl.error.base import (
    PgRepositoryInputIsNotDataclass,
    PgRepositoryMissingSqlParameter
)

GenericInputClass = TypeVar("GenericInputClass")
M = TypeVar("M")

class NvSql:
    @classmethod
    def literal(*args):
        concat = []
        for i in args:
            concat.append(i)
        return ''.join(concat)

class ModelRowFactory:
    def __init__(
        self, 
        listOrderFields: list[ModelField],
        /, *,
        modelReturn: Optional[Type[M]] = None
    ):
        self.fields = listOrderFields
        self.returningModel = modelReturn

    def __call__(
        self, 
        *args: Sequence[Any]
    ) -> dict[str, Any] | dict[Type[M], M]:
        if len(args) == 0:
            raise Exception("RowFactory is been called with no parameters.")
        if len(args) > 0 and isinstance(args[0], Cursor):
            return self

        values: Sequence[Any] = args[0]
        eachModel: dict[str, Any] = {}
        instancesModel: dict[object, object] = {}
        retObject: M = None

        for i in range(len(values)):
            field = self.fields[i]
            modelData = field.owner.__model_data__
            if modelData not in eachModel:
                eachModel[modelData] = {}
            eachModel[modelData].update({ field.attr: values[i] })

        #TODO: I don't know if I want to continue this. I think the default is working OK, at least for now.
        if self.returningModel:
            retObject = self.returningModel()

            for model in eachModel.keys():
                if not retObject.__dict__.get(model):
                    raise Exception("Model assigned to return the query doesn't exists as a type of returned query.")

                for attr in retObject.__dict__.keys():
                    if isinstance(retObject.__dict__[attr], model):
                        setattr(retObject, attr, model(**eachModel[model])) 
            
            instancesModel[self.returningModel] = retObject
            return instancesModel
        
        for model in eachModel.keys():
            instancesModel[model] = model(**eachModel[model])

        return instancesModel
        
        return dict(zip(self.fields, values))

class PgRepositoryBase:

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
        auditObject: GenericInputClass = None
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
                    inputFieldValue = auditObject.__getattribute__(paramAttr)
                else:
                    inputFieldValue = inputObject.__getattribute__(paramAttr)
            except AttributeError as e:
                raise PgRepositoryMissingSqlParameter(
                    "Param has no input field. Please verify the input and audit objects."
                )

            paramAssigned[paramAttr] = inputFieldValue

        return paramAssigned

    #TODO: use metadata to assign the values from select