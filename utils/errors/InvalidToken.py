from discord import Member, User


class InvalidToken(Exception):
    def __init__(self, user: User | Member) -> None:
        super().__init__()
        self.user = user
