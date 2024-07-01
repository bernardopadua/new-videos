# BUILT-IN
from datetime import date

# SERVICES
from nvideos_web.services.base_service import BaseService
from nvideos_web.services.user.error import UserServiceNoUserInput

# ENTITY
from nvideos_web.core.entity.user import User, UserInput
from nvideos_web.core.entity.constants import UserPermissions

# REPOSITORY
from nvideos_web.impl.user_repository import PgUserRepository, PasswordHasher

# DB
from nvideos_web.db.pgcontext import NewVideosDBContext
# Used to perform test with single connection
#from nvideos_web.db.pgcontext_perf_test import NewVideosDBContext

class UserService(BaseService):

    def __init__(self, currentUser: int) -> None:
        super().__init__(currentUser=currentUser)
        self._usuRep = PgUserRepository(dbContext=NewVideosDBContext)

        self._inputUser: UserInput

    def createNewUser(self, *, userInput: UserInput | None = None) -> User:
        self.insertingMode()
        auditData = self.fillAuditData()
        userInput = userInput if userInput else self._inputUser

        if not userInput:
            raise UserServiceNoUserInput(
                "No user input. Verify if you are setting the user input."
            )

        self._usuRep.create(
            userInputData=userInput, 
            auditInputData=auditData
        )

    def perfShow(self, seconds: int):
        print(seconds)

        result = self._usuRep.perfGetUserById(seconds=seconds)
        
        return f"""
            <h3>
                <br>
                repo:: {id(self._usuRep)}
                <br>
                id:: {id(self)}
                <br>
                result:: {result}
            </h3>            
        """

    def setUserInput(
        self, 
        userName: str = "",
        userEmail: str = "",
        userSurname: str = "",
        userAvatarUrl: str = "",
        userBirthDate: date | None = None,
        userPassword: str = "",
        createSystemUser: bool = False
    ) -> UserInput:
        if not userBirthDate:
            userBirthDate = date.today()

        userPerm = UserInput.userPermission
        if createSystemUser:
            userPerm = UserPermissions.P_SYSTEM.value
        
        passwordHash = PasswordHasher().hashPassword(
            userPassword
        )

        self._inputUser = UserInput(
            userName=userName,
            userSurname=userSurname,
            userEmail=userEmail,
            userPassword=passwordHash,
            userBirthDate=userBirthDate,
            userAvatarUrl=userAvatarUrl,
            userPermission=userPerm,
            userIsActive=True
        )

        return self._inputUser