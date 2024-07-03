# is running from virtualenv ?
import sys
from os import environ
from pathlib import Path
avoidENVCheck = environ.get("AVOID_VIRTUALENV_CHECK", "False").lower()=="true"
if sys.prefix != sys.base_prefix and not avoidENVCheck:
    #avoiding problems with no migration module
    sys.path.append(Path(__file__).parent.parent.__str__())

from argparse import ArgumentParser

from nvideos_web.services.user.service import UserService

parser = ArgumentParser(description="new-videos CLI tool")
parser.add_argument("-iu", 
    "--insert-user", 
    action="store_true", help="Insert a system user to database"
)

def insertNewUser():
    from datetime import date
    print("For now I'm just hoping you are not informed no empty fields!\n")
    userName = input("UserName: ")
    userEmail = input("UserEmail: ")
    userPassword = input("UserPassword: ")
    
    print("UserBirthDate: \n")
    day   = int(input("Day: "))
    month = int(input("Month: "))
    year  = int(input("Year: "))

    user = UserService().setUserInput(
        userName=userName,
        userEmail=userEmail,
        userPassword=userPassword,
        userBirthDate=date(year=year, month=month, day=day),
        createSystemUser=True
    ).createNewUser()

    print("\nUser created::")
    user.print()

def main():
    args = parser.parse_args()

    if args.insert_user:
        insertNewUser()

if __name__=="__main__":
    main()