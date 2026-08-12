# PSYCOPG
from psycopg.rows import RowMaker
from psycopg.cursor import Cursor

# TYPING
from typing import (
    Any
)
from collections.abc import Sequence

# ENTITY
from nvideos_web.core.entity.base.base_entity import ModelField, BaseModelData

class ModelRowFactory:
    def __init__(
        self, 
        listOrderFields: list[ModelField],
        /, *, additionalModelFields: type[BaseModelData] | None = None
    ):
        self.fields: list[ModelField] = listOrderFields
        self._additionalModelFields: type[BaseModelData] | None = additionalModelFields

    def __call__(
        self, 
        cursor: Cursor
    ) -> RowMaker[dict[int, Any]]:

        def make_row(values: Sequence[Any], /) -> dict[int, Any]:
            eachModel: dict[int, dict[str, Any]] = {}
            instancesModel: dict[int, object] = {}

            for i in range(len(values)):
                if i < len(self.fields):
                    field: ModelField = self.fields[i]
                    modelIdentification: int = id(field.getOwner())
                    if modelIdentification not in eachModel:
                        eachModel[modelIdentification] = { "model": field.getOwner().modelData() , "row": {} }
                    if values[i] is not None and values[i] != "":
                        eachModel[modelIdentification]["row"][field.attr] = values[i]
                elif self._additionalModelFields is not None:
                    modelIdentification: int = id(self._additionalModelFields)
                    fieldStr: str
                    if cursor and cursor.description and cursor.description[i]:
                        fieldStr = cursor.description[i].name
                        eachModel[modelIdentification] = { "model": self._additionalModelFields, "row": {} }
                        eachModel[modelIdentification]["row"][fieldStr] = values[i]

            for model in eachModel.keys():
                modelData = eachModel[model]["model"]
                instancesModel[model] = modelData(**eachModel[model]["row"])

            return instancesModel
        return make_row

    @classmethod
    def getRowFactory(
        cls, 
        listOrderFields: list[ModelField]
    ) -> "ModelRowFactory":
        return cls(listOrderFields)
