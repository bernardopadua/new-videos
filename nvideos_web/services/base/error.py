class InputDataIsNone(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
    @staticmethod
    def genericError() -> str:
        return "Input data is None and it cannot happen."