class PgRepositoryException(Exception):
    pass

class PgRepositoryMissingParameter(PgRepositoryException):
    pass

class PgRepositoryMissingSqlParameter(PgRepositoryException):
    pass

class PgRepositoryInputIsNotDataclass(PgRepositoryException):
    pass

class PgRepositoryParameterValueNone(PgRepositoryException):
    pass
