from dataclasses import field, dataclass

from nvideos_web.core.entity.base_entity import ModelField

METADATA_FIELD_NAME = "dbfield"

def setUpMetadata(column: ModelField):
    return {
        METADATA_FIELD_NAME: column.field
    }

def setUpField(column: ModelField, **kwargs):
    result = {}
    result[METADATA_FIELD_NAME] = column.field
    return field(metadata=result, **kwargs)

@dataclass
class MappingModel:
    def to_json(self):
        pass