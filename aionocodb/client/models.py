class APIToken:
    def __init__(self, token: str):
        self.__token = token

    def get_header(self) -> dict:
        return {"xc-token": self.__token}


class JWTAuthToken:
    def __init__(self, token: str):
        self.__token = token

    def get_header(self) -> dict:
        return {"xc-auth": self.__token}
    

class Project:
    def __init__(self, project_org: str, project_name: str):
        self.project_org = project_org
        self.project_name = project_name