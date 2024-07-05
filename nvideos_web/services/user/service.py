# BUILT-IN
from datetime import date

# TYPING
from typing import Any, Type

# SERVICES
from nvideos_web.services.base_service import BaseService
from nvideos_web.services.user.error import UserServiceNoUserInput

# ENTITY
from nvideos_web.core.entity.user import User, UserInput, AuditData
from nvideos_web.core.entity.base.constants import UserPermissions

# REPOSITORY
from nvideos_web.impl.user_repository import PgUserRepository, PasswordHasher

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext
# Used to perform test with single connection
#from nvideos_web.db.pgcontext_perf_test import NewVideosDBContext

# ERROR
from nvideos_web.services.base.error import InputDataIsNone

class UserService(BaseService["UserService", UserInput]):
    def __init__(
        self, 
        *,
        userId: int | None = None, 
        dbContext: Type[NewVideosDBContext] | None = None
    ) -> None:
        super().__init__(currentUser=userId)
        #mypy doesn't understand inline if
        if dbContext is None:
            dbContext=NewVideosDBContext
            
        self._usuRep = PgUserRepository(dbContext=dbContext)

    def createNewUser(self, *, userInput: UserInput | None = None) -> User:
        self.insertingMode()
        auditData = self.fillAuditData().getAuditData()
        userInput = userInput if userInput else self._filledInputData

        if not userInput:
            raise UserServiceNoUserInput(
                "No user input. Verify if you are setting the user input."
            )
        try:
            return self._usuRep.create(
                userInputData=userInput, 
                auditInputData=auditData
            )
        finally:
            self.resetData()

    def updateUserById(
        self, 
        userId: int,
        /, *, 
        userInput: UserInput | None = None
    ) -> User:
        auditData = self.fillAuditData().getAuditData()
        inputData = self.getInputData()

        try:
            return self._usuRep.updateById(
                userId=userId,
                newUserData=inputData, 
                auditData=auditData
            )
        finally:
            self.resetData()

    def deleteByUserId(self, userId: int) -> User:
        if self._currentUser is None:
            raise Exception("Current user cannot be None for deletion of user. It must maintain audit data.")
        try:
            self.fillAuditData()
            return self._usuRep.delete(userId=userId, auditData=self.getAuditData())
        finally:
            self.resetData()

    def getInputData(self) -> UserInput:
        if self._filledInputData is None:
            raise InputDataIsNone(InputDataIsNone.genericError())
        return self._filledInputData

    def fillInputData(
        self, 
        /, *,
        userName: str | None = None,
        userEmail: str | None = None,
        userSurname: str | None = None,
        userAvatarUrl: str | None = None,
        userBirthDate: date | None = None,
        userPassword: str | None = None,
        userPermission: str | None = None,
        userIsActive: bool | None = None,
        createSystemUser: bool = False,
        fillTodayData: bool = False
    ) -> "UserService":
        if not userBirthDate and fillTodayData:
            userBirthDate = date.today()

        userPerm: str | None = None
        if createSystemUser:
            userPerm = UserPermissions.P_SYSTEM.value
        elif userPermission:
            userPerm = userPermission
        
        passwordHash: str | None = userPassword
        if userPassword is not None:
            passwordHash = PasswordHasher().hashPassword(
                userPassword
            )

        self._filledInputData = UserInput(
            userName=userName,
            userSurname=userSurname,
            userEmail=userEmail,
            userPassword=passwordHash,
            userBirthDate=userBirthDate,
            userAvatarUrl=userAvatarUrl,
            userPermission=userPerm,
            userIsActive=userIsActive
        )

        return self