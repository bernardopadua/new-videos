# BUILT-IN
from datetime import timezone

# TYPING
from typing import Generic, TypeVar

# ENTITY
from nvideos_web.core.entity.base_entity import AuditData

TInputData = TypeVar("TInputData")

class BaseService(Generic[TInputData]):
    def __init__(self, currentUser: int | None) -> None:
        self._currentUser: int | None = currentUser
        
        self._filledInputData: TInputData | None = None
        self._filledAudit: AuditData | None = None

        self._insertingMode: bool = False
        self._updatingMode: bool = False

    @property
    def currentUser(self) -> int | None:
        return self._currentUser

    def insertingMode(self):
        self._insertingMode = True
    def updatingMode(self):
        self._updatingMode = True

    def getAuditData(self) -> AuditData:
        if self._filledAudit is None:
            raise Exception("Audit data has to be filled before get")
        return self._filledAudit

    def fillAuditData(
        self, /, *, 
        createdBy: int | None = None, 
        updatedBy: int | None = None
    ) -> "BaseService":
        from datetime import datetime

        if self._insertingMode:
            self._filledAudit = AuditData(
                self.currentUser if not updatedBy else updatedBy,
                self.currentUser if not createdBy else createdBy,
                datetime.now(timezone.utc),
                datetime.now(timezone.utc)
            )
            self._insertingMode = False
        else:
            self._filledAudit = AuditData(
                self.currentUser if not updatedBy else updatedBy,
                None,
                None,
                datetime.now(timezone.utc)
            )
        
        return self
    
    def resetData(self):
        self._filledAudit = None
        self._filledInputData = None