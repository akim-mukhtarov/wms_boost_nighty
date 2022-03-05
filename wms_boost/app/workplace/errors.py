from fastapi import HTTPException


class WorkplaceNotFound(HTTPException):

    _status_code = 404
    _msg = "Workplace with provided id does not exist"

    def __init__(self):
        super().__init__(self._status_code, detail=self._msg)
