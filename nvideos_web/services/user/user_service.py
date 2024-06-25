from dataclasses import dataclass

from datetime import date

from nvideos_web.core.entity.user import User, NewUserInput
from nvideos_web.core.entity.constants import UserPermissions
from nvideos_web.impl.user_repository import PgUserRepository, PasswordHasher
from nvideos_web.db.pgcontext import NewVideosDBContext
# Used to perform test with single connection
#from nvideos_web.db.pgcontext_perf_test import NewVideosDBContext

class UserService:

    def __init__(self) -> None:
        self._usuRep = PgUserRepository(dbContext=NewVideosDBContext)

    def createNewUser(self, userInput: NewUserInput) -> User:
        self._usuRep.create()
        pass

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
    
    @classmethod
    def getDateNow(cls) -> date:
        return date.today()

    @classmethod
    def getNewUserInput(
        cls, 
        userName: str = "",
        userEmail: str = "",
        userSurname: str = "",
        userAvatarUrl: str = "",
        userBirthDate: date = None,
        userPassword: str = "",
        createSystemUser: bool = False
    ) -> NewUserInput:
        if not userBirthDate:
            userBirthDate = cls.getDateNow()

        userPerm = NewUserInput.userPermission
        if createSystemUser:
            userPerm = UserPermissions.P_SYSTEM.value
        
        passwordHash = PasswordHasher().hashPassword(
            userPassword
        )

        nInput = NewUserInput(
            userName=userName,
            userSurname=userSurname,
            userEmail=userEmail,
            userPassword=passwordHash,
            userBirthDate=userBirthDate,
            userAvatarUrl=userAvatarUrl,
            userPermission=userPerm,
            userIsActive=True
        )

        return nInput