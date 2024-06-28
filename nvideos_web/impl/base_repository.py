from typing import NewType, Sequence, Any
from psycopg import _queries

from dataclasses import is_dataclass

from nvideos_web.core.entity.entity_base import ModelField
from nvideos_web.impl.error.base import (
    PgRepositoryInputIsNotDataclass,
    PgRepositoryMissingSqlParameter
)

GenericInputClass = NewType("GenericInputClass", type)

class NvSql:
    @classmethod
    def literal(*args):
        concat = []
        for i in args:
            concat.append(i)
        return ''.join(concat)

# class DictRowFactory:
#     def __init__(
#         self, 
#         #cursor
#         listOrderFields: list[ModelField]
#     ):
#         #self.fields = [c.name for c in cursor.description]
#         self.fields = listOrderFields

#     def __call__(
#         self, 
#         #values: Sequence[Any],
#         *args
#     ) -> dict[str, Any]:
#         if len(args) <= 1:
#             self._s = args[0]
#             return
        
#         eachModel: dict[str, Any] = {}
#         instancesModel: dict[object, object] = {}
#         values = []

#         for i in values:
#             field = self.fields[i]
#             if field.owner not in eachModel:
#                 eachModel[field.owner] = {}
#             eachModel[field.owner].update({ field.attr: values[i] })

#         for model in eachModel.keys():
#             instancesModel[model] = model(**eachModel[model])

#         return dict(zip(self.fields, values))

def makeRowFactory(listFieldsOrder: list[ModelField]):
    listFieldsOrder = listFieldsOrder
    class DictRowFactory:
        def __init__(
            self, 
            cursor
            #listOrderFields: list[ModelField]
        ):
            #self.fields = [c.name for c in cursor.description]
            self.fields = listFieldsOrder

        def __call__(
            self, 
            #values: Sequence[Any],
            *args
        ) -> dict[str, Any]:
            eachModel: dict[str, Any] = {}
            instancesModel: dict[object, object] = {}
            values = []

            for i in values:
                field = self.fields[i]
                if field.owner not in eachModel:
                    eachModel[field.owner] = {}
                eachModel[field.owner].update({ field.attr: values[i] })

            for model in eachModel.keys():
                instancesModel[model] = model(**eachModel[model])

            return dict(zip(self.fields, values))
    
    return DictRowFactory

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