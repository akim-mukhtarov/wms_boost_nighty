from typing import Tuple
from contextlib import contextmanager


class SheetsService:
    """ API of service that handles all requests
        to Google SpreadSheets API """
    class Connection:
        def send(self, method_name: str, args: Tuple) -> None:
            pass

        def close(self) -> None:
            pass

    @classmethod
    def append(cls, sheet_url: str, data) -> int:
        with cls._connect() as conn:
            conn.send("append", (sheet_url, data))
        return len(data)

    @classmethod
    @contextmanager
    def _connect(cls):
        try:
            conn = SheetsService.Connection()
            yield conn

        except Exception:
            conn.close()
            raise e

        finally:
            conn.close()
