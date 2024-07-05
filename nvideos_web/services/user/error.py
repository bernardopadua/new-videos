class UserServiceNoUserInput(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class UserServiceUserDoesntExists(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
