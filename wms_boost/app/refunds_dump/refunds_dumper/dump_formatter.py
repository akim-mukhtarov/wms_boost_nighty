from typing import TypeVar, Dict, List
from app.wms_api.models import ReadyRefunds


RefundDict = TypeVar('RefundDict', bound=Dict)

class DumpFormatter:
    """ Parse refund info from wms' `Refund` """
    def __init__(self, user: User, workplace: Workplace):
        pass

    def format_all(self, refunds: List[ReadyRefunds.Refund]) -> List[RefundDict]:
        pass

    def format(self, refund: Refund) -> RefundDict:
        pass
