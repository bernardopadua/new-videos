from dataclasses import field, dataclass

METADATA_FIELD_NAME = "dbfield"

def setUpMetadata(column: str):
    return {
        METADATA_FIELD_NAME: column
    }

def setUpField(column: str, **kwargs):
    result = {}
    result[METADATA_FIELD_NAME] = column
    return field(metadata=result, **kwargs)

@dataclass
class MappingModel:
    def to_json(self):
        pass