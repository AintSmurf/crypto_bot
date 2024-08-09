import os


class CredentialsUtility:
    def __init__(self) -> None:
        self.public_key = ""
        self.secret_key = ""

    def get_api_keys(self):
        self.public_key = os.environ["PUBLIC_KEY"]
        self.secret_key = os.environ["SECRET_KEY"]
        return {"PUBLIC_KEY": self.public_key, "SECRET_KEY": self.secret_key}
