

class AuthenticationError(Exception):
    pass

class UnexpectedApiResponse(Exception):
    def __init__(self, url: str=None, payload=None):
        self.url=url
        self.payload=payload

class WmsServerError(Exception):
    def __init__(self, url: str, status_code: int):
        self.url=url
        self.status_code=status_code
