from itertools import islice

from app.models import User, Workplace
from app.refunds_dump.today_dump import TodayDump
from app.wms_api import WmsApi as wms
from app.sheets_service import SheetsService

from .errors import AlreadyProcessed
from .utils import barcode_required, insert_barcodes


class RefundsDumper:

    def __init__(self, user: User, workplace: Workplace):
        self._user = user
        self._workplace = workplace
        self._today_dump = TodayDump(workplace)

    def _get_ready_refunds(self, offset: int=0):
        """  Fetch ready refunds with given offset """
        refunds = wms.get_ready_refunds(user.wms_access_token, wms_key)
        return islice(refunds.iter_items, offset, len(refunds))

    def _get_data_to_dump(self) -> List[Dict]:
        """ Fetch ready refunds from wms with given offset
            return parsed and formated for dump """
        refunds = []        # parsed refunds info to dump
        sku_ids = {}        # map sku id of refund to refund itself

        items = self._get_ready_refunds(offset=self._today_dump.included)

        for item in items:
            refund = parse_refund(item)
            if barcode_required(item):
                sku_ids[item.sku] = refund

        if len(sku_ids):
            products_info = wms.get_products_info(
                    self._user.wms_access_token,
                    sku_ids.values())
            insert_barcodes(refunds, products_info, sku_ids)
        return refunds

    def dump(self) -> int:
        """ Enqueue the task for dumping refunds
            return quantity of items to be included """
        status = self._today_dump.status
        if status == 'enqueued':
            raise AlreadyProcessed()

        already_included = self._today_dump.included
        wms_key = self._today_dump.workplace_id
        refunds = self._get_data_to_dump()

        just_included = SheetsService.append(
                            self._today_dump.report_url,
                            refunds)

        self._today_dump.add_new(just_included)
        return just_included
