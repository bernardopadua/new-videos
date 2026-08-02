# PSYCOPG
from psycopg import Cursor
from psycopg.rows import RowMaker

# TYPING
from typing import (
    Any, Sequence
)

# ENTITY
from nvideos_web.core.entity.base.base_entity import ModelField

class ModelRowFactory(RowMaker):
    def __init__(
        self, 
        listOrderFields: list[ModelField],
    ):
        self.fields = listOrderFields

    def __call__(
        self, 
        *args: Sequence[Any]
    ) -> dict[int, Any] | "ModelRowFactory":
        if len(args) == 0:
            raise Exception("RowFactory is been called with no parameters.")
        if len(args) > 0 and isinstance(args[0], Cursor):
            return self

        values: Sequence[Any] = args[0]
        eachModel: dict[int, dict[str, Any]] = {}
        instancesModel: dict[int, object] = {}
        
        #TODO: I dont know if I will be implementing this yet. 
        #The idea is to return a different value-object and assemble this special case object at this step.
        #>>>>>>>>> retObject: M = None

        for i in range(len(values)):
            field: ModelField = self.fields[i]
            modelIdentification: int = id(field.getOwner())
            if modelIdentification not in eachModel:
                eachModel[modelIdentification] = { "model": field.getOwner().modelData() , "row": {} }
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
        cls: type["ModelRowFactory"], 
        listOrderFields: list[ModelField]
    ) -> "ModelRowFactory":
        return cls(listOrderFields)
