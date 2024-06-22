from datetime import datetime
from dataclasses import dataclass

@dataclass
class BaseFieldsMixin:
    updated_by: int
    create_by: int
    created_at: datetime
    updated_at: datetime
