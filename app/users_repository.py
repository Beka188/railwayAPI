from attrs import define


@define
class User:
    email: str
    full_name: str
    hashed_password: bytes = ''
    id: int = 0


class UsersRepository:
    users: list[User]

    def __init__(self):
        self.users = []

    # необходимые методы сюда
    def add_user(self, email, full_name, hashed_password):
        user = User(email, full_name, hashed_password)
        self.users.append(user)

    def get_password(self, email):
        for user in self.users:
            if user.email == email:
                return user.hashed_password
        return None

    def get_user(self, email):
        for user in self.users:
            if user.email == email:
                return user
        return None

    def get_users(self):
        return self.users
    # конец решения
