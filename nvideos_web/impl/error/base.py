class PgRepositoryMissingParameter(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PgRepositoryMissingSqlParameter(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class PgRepositoryInputIsNotDataclass(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
