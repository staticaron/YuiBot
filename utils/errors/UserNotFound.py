from discord import Member, User, errors


class UserNotFound(errors.ClientException):
    def __init__(self, user: User | Member | None = None, user_id=None) -> None:
        """
        Pass either of user or user_id
        """
        super().__init__()
        self.user = user
        self.user_id = user_id
