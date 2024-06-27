from typing import NewType
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

class PgRepositoryBase:

    def sqlFields(self, *args: ModelField) -> str:
        concat = []
        for arg in args:
            concat.append(arg)
        return ','.join(concat)

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