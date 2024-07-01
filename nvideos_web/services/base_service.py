from datetime import date
from nvideos_web.core.entity.base_entity import AuditData

class BaseService:
    def __init__(self, currentUser: int) -> None:
        self._currentUser: int = currentUser
        self._filledAudit: AuditData | None = None

        self._insertingMode: bool = False

    def insertingMode(self):
        self._insertingMode = True

    def fillAuditData(
        self, /, *, 
        createdBy: int | None = None, 
        updatedBy: int | None = None
    ) -> AuditData:
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