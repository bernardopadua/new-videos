class ChannelServiceCurrentUserIsNone(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ChannelServiceChannelDoesntExists(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)