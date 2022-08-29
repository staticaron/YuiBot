from discord import Member

class InvalidToken(Exception):

    user:Member = None

    def __init__(self, user:Member) -> None:
        super().__init__()
        self.user = user