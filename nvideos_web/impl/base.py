from typing import NewType
from psycopg import _queries

from dataclasses import is_dataclass, Field

from nvideos_web.core.entity.metadata import METADATA_FIELD_NAME
from nvideos_web.impl.error.base import (
    PgRepositoryInputIsNotDataclass,
    PgRepositoryMissingParameter,
    PgRepositoryFieldMissingMetadata
)

GenericInputClass = NewType("GenericInputClass", type)

class PgRepositoryBase:

    def parseSqlParams(self, _sql: str, inputObject: GenericInputClass) -> dict:
        if not is_dataclass(inputObject):
            raise PgRepositoryInputIsNotDataclass(
                "Object passed to parsing params is not dataclass."
            )

        paramAssigned = {}
        sqlParams = _queries._re_placeholder.finditer(
            bytes(_sql.encode('utf-8'))
        )
        for param in sqlParams:
            try:
                inputFieldValue = inputObject.__getattribute__(param)
            except AttributeError as e:
                raise PgRepositoryMissingParameter(
                    "Param has no input field. Please verify the input object."
                )
            paramAssigned[param] = inputFieldValue

    #TODO: use metadata to assign the values from select