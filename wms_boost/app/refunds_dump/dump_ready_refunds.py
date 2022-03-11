from typing import List, Dict

from app.models import User, LastRefundsDump
from app.wms_api.models import Refund, ReadyRefunds
from app.wms_api import WmsApi as wms
from app.sheets_service import SheetsService

from .errors import AlreadyProcessed
from .last_dump import LastDump
from .today_dump import TodayDump


def _get_ready_refunds(user: User, wms_key: int, offset: int=0):
    refunds = wms.get_ready_refunds(user.wms_access_token, wms_key)
    return islice(refunds.iter_items, offset, len(refunds))


def _insert_barcodes(refunds, products_info, sku_ids) -> None:
    for item in products_info.iter_items():
        refund = sku_ids.get(item.sku_id)
        refund['barcode'] = item.barcode

# TODO: implement
def _parse_refund(refund: Refund) -> Dict:
    pass

# TODO: implement
def _barcode_required(refund: Dict) -> bool:
    pass


def _get_data_to_dump(
        user: User,
        wms_key: int,
        already_included: int=0
) -> List[Dict]:
    """ Fetch ready refunds from wms with given offset
        return parsed and formated for dump """
    refunds = []        # parsed refunds info to dump
    sku_ids = {}        # map sku id of refund to refund itself

    items = _get_ready_refunds(user, wms_key, already_included)

    for item in items:
        refund = _parse_refund(item)
        if _barcode_required(item):
            sku_ids[item.sku] = refund

    if len(sku_ids):
        products_info = wms.get_products_info(
                user.wms_access_token,
                sku_ids.values())
        return _insert_barcodes(refunds, products_info, sku_ids)

    return refunds


def dump_ready_refunds(user: User, today_state: TodayDump) -> int:
    """ Enqueue the task for dumping refunds """
    status = today_state.status
    if status == 'enqueued':
        raise AlreadyProcessed()

    already_included = today_state.included
    wms_key = today_state.workplace_id
    refunds = _get_data_to_dump(user, wms_key, already_included)

    just_included = SheetsService.append(today_state.report_url, refunds)
    today_state.add_new(just_included)

    return just_included
