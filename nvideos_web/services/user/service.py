# FLASK
from flask import current_app as app, session

# BUILT-IN
from datetime import date, datetime

# TYPING
from typing import Self, override, final

# SERVICES
from nvideos_web.services.base.service import BaseService
from nvideos_web.services.user.error import (
    UserServiceNoUserInput, UserServiceUserDoesntExists,
    UserServiceUserDontMatchPassword, UserServiceUserNameTooShort,
    UserServiceUserHasInvalidPassword, UserServiceUserHasInvalidEmail,
    UserServiceDateIsInvalid, UserServiceUserHasInvalidPermission,
    UserServiceFailedToMoveTempAvatarToMedia, UserServiceUserHasInvalidBirthDate
)

# ENTITY
from nvideos_web.core.entity.user import User, UserInput
from nvideos_web.core.entity.base.constants import UserPermissions

# REPOSITORY
from nvideos_web.impl.user_repository import PgUserRepository, PasswordHasher

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext
# Used to perform test with single connection
#from nvideos_web.db.pgcontext_perf_test import NewVideosDBContext

# ERROR
from nvideos_web.services.base.error import InputDataIsNone

@final
class UserService(BaseService[UserInput]):
    def __init__(
        self, 
        *,
        userId: int | None = None, 
        dbContext: type[NewVideosDBContext] | None = None
    ) -> None:
        super().__init__(currentUser=userId)
        #mypy doesn't understand inline if
        if dbContext is None:
            dbContext=NewVideosDBContext
            
        self._usuRep: PgUserRepository = PgUserRepository(dbContext=dbContext)
        self._userPerm: str | None = None
        self._userAvatarUrl: str | None = None

    def selectByUserName(self, userName: str) -> User:
        return self._usuRep.selectByUserName(userName)
    
    def selectByUserEmail(self, userEmail: str) -> User:
        return self._usuRep.selectByUserEmail(userEmail)
    
    def selectByUserId(self, userId: int | None = None) -> User:
        if self.currentUser and userId is None:
            userId = self.currentUser

        return self._usuRep.selectByUserId(userId)

    def userEmailExists(self, userEmail: str) -> bool:
        if self.currentUser:
            return self._usuRep.userEmailExists(userEmail, avoidMyself=self.currentUser)
        else:
            return self._usuRep.userEmailExists(userEmail)

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

    def checkInputDataIsValid(self) -> Self:
        if self._filledInputData is None:
            raise UserServiceNoUserInput(
                "No user input. Verify if you are setting the user input."
            )

        def checkForSpecialChars(text:str) -> bool:
            import re
            return bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", text))

        def checkForValidEmail(email: str) -> bool:
            import re
            return bool(re.search(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))


        if self._filledInputData.userPasswordPlain != self._filledInputData.confirmPassword:
            raise UserServiceUserDontMatchPassword("The informed password doesn't match the user's password.")
        
        if self._filledInputData.userName is not None and len(self._filledInputData.userName) < 3:
            raise UserServiceUserNameTooShort("The informed user name is too short or is None.")
        
        if self._filledInputData.userSurname is not None and len(self._filledInputData.userSurname) < 3:
            raise UserServiceUserNameTooShort("The informed user surname is too short or is None.")

        if self._filledInputData.userPasswordPlain is not None and \
        checkForSpecialChars(self._filledInputData.userPasswordPlain):
            raise UserServiceUserHasInvalidPassword("The informed password has invalid characters.")

        if self._filledInputData.userEmail is not None and not checkForValidEmail(
            self._filledInputData.userEmail
        ):
            raise UserServiceUserHasInvalidEmail("The informed email is invalid.")

        if self._filledInputData.userPermission is None and self.isInsertingMode():
            raise UserServiceUserHasInvalidPermission("The informed permission is invalid.")

        if self._filledInputData.userBirthDate is None or \
            (datetime.now().year - self._filledInputData.userBirthDate.year) < 18:
            raise UserServiceUserHasInvalidBirthDate("The informed user birth date is invalid. The user must be at least 18 years old.")

        if self._filledInputData.userEmail is None:
            raise UserServiceUserHasInvalidEmail("User email cannot be None.")

        if self.userEmailExists(self._filledInputData.userEmail):
            #This is dangerous as a point of check emails in this database.
            #I could only register and confirm email and etc. But I will keep it. 
            #This project is only a exercise. A service to check email is worst because of "ddos".
            raise UserServiceUserHasInvalidEmail("The informed email already exists.")

        return self

    @override
    def checkIdExists(self, idRegistry: int) -> Self:
        self._checkExists: bool = self._usuRep.checkIdExists(userId=idRegistry)
        return self

    def setUserPermission(self, *, systemUser: bool = False, normalUser: bool = False) -> Self:
        if systemUser:
            self._userPerm = UserPermissions.P_SYSTEM.value
        elif normalUser:
            self._userPerm = UserPermissions.P_COMMOM_USER.value
        else:
            self._userPerm = None
        return self

    def updateUserById(
        self, 
        userId: int,
        /, *, 
        updatedByUserId: int | None = None
    ) -> User:
        self.updatingMode()
        auditData = self.fillAuditData(
            updatedBy=self.currentUser if self.currentUser else updatedByUserId
        ).getAuditData()
        inputData = self.getInputData()

        try:
            if not self.checkIdExists(idRegistry=userId).getCheckIdExists():
                raise UserServiceUserDoesntExists("The user you trying to update doesn't exists")

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
        audiData = self.fillAuditData().getAuditData()

        try:
            if not self.checkIdExists(userId=userId).getCheckIdExists():
                raise UserServiceUserDoesntExists("The user you trying to update doesn't exists")

            return self._usuRep.delete(userId=userId, auditData=audiData)
        finally:
            self.resetData()

    @override
    def getInputData(self) -> UserInput:
        if self._filledInputData is None:
            raise InputDataIsNone(InputDataIsNone.genericError())
        return self._filledInputData

    @override
    def fillInputData(
        self, 
        /, *,
        userName: str | None = None,
        userEmail: str | None = None,
        userSurname: str | None = None,
        userAvatarUrl: str | None = None,
        userBirthDate: date | None = None,
        userPassword: str | None = None,
        confirmPassword: str | None = None,
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
        elif self._userPerm:
            userPerm = self._userPerm
            self._userPerm = None
        
        if self._userAvatarUrl is not None:
            userAvatarUrl = self._userAvatarUrl
            self._userAvatarUrl = None

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
            userPasswordPlain=userPassword,
            confirmPassword=confirmPassword,
            userBirthDate=userBirthDate,
            userAvatarUrl=userAvatarUrl,
            userPermission=userPerm,
            userIsActive=userIsActive
        )

        return self

    def getDatetimeFromDate(self, dateStr: str | None) -> datetime:
        if dateStr is None:
            raise UserServiceDateIsInvalid("The date is None.")

        try:
            return datetime.strptime(dateStr, "%Y-%m-%d")
        except Exception as e:
            #TODO: LOG: Logging e
            raise e

    def moveTempAvatarToMedia(self, userId: int, avatarTempName: str | None) -> Self:
        # I maintaning this request because is a simple task, is not CPU bound is just a MOVE.
        from urllib.request import Request, urlopen
        from urllib.error import HTTPError
        from typing import cast
        import json

        req: Request = Request(
            url=f"{app.config['DOMAIN_MEDIA_SERVER']}/upload/move/avatar/user/{userId}/{avatarTempName}", 
            method="POST"
        )
        try:
            with urlopen(req) as response:
                bResponse: bytes = cast(bytes, response.read())
                jResponse: dict[str, str] = json.loads(bResponse.decode("utf-8"))
                self._userAvatarUrl = app.config['DOMAIN_MEDIA_SERVER']+jResponse.get("userAvatarUrl")
                return self
        except HTTPError:
            #add logger
            #_: bytes = e.read()
            raise UserServiceFailedToMoveTempAvatarToMedia("The media server couldn't move the temp avatar to media.")

    def userLogin(self, email: str, password: str) -> User | None:
        userData: User = self.selectByUserEmail(email)

        if PasswordHasher().hashPassword(password) == userData.userPassword:
            self.fillUserSession(userData)

            return userData
        
        return None

    def fillUserSession(self, userData: User):
        session["userId"] = userData.userId
        session["user"] = {
            "userId": userData.userId,
            "userName": userData.userName,
            "userSurname": userData.userSurname,
            "userEmail": userData.userEmail,
            "userAvatarUrl": userData.userAvatarUrl
        }
