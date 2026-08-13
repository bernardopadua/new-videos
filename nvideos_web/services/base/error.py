class ServiceException(Exception):
    pass

class InputDataIsNone(ServiceException):
    @staticmethod
    def genericError() -> str:
        return "Input data is None and it cannot happen."