from discord import errors, Member

class UserNotFound(errors.ClientException):
    def __init__(self, user:Member=None, user_id=None) -> None:
        super().__init__()
        self.user = user
        self.user_id = user_id