

class AlreadyProcessed(Exception):
    _msg = "Refunds dump is already being processed"

    def __init__(self):
        super().__init__(self._msg)
