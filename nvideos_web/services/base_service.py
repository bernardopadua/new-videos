from datetime import date
from nvideos_web.core.entity.base_entity import AuditData

class BaseService:
    def __init__(self, currentUser: int = None) -> None:
        self._currentUser = currentUser
        self._filledAudit = None

        self._insertingMode = False

    def insertingMode(self):
        self._insertingMode = True

    def fillAuditData(self, *, createdBy:int = None, updatedBy:int = None) -> AuditData:
        from datetime import datetime

        if self._insertingMode:
            self._filledAudit = AuditData(
                self._currentUser if not updatedBy else updatedBy,
                self._currentUser if not createdBy else createdBy,
                datetime.now(),
                datetime.now()
            )
            self._insertingMode = False
        else:
            self._filledAudit = AuditData(
                self._currentUser if not updatedBy else updatedBy,
                None,
                None,
                datetime.now()
            )
        
        return self._filledAudit