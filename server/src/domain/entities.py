class User:
    def __init__(self, username: str, password: str, enabled: bool):
        self.username = username
        self.password = password
        self.enabled = enabled