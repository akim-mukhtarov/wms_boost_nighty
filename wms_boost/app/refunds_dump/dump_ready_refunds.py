from app.models import User, LastRefundsDump
from app.wms_api.models import Refund, ReadyRefunds
from app.wms_api import WmsApi as wms
from app.sheets_service import SheetsService
from app.refuns_dump import TodayDump

from .errors import AlreadyProcessed
from .last_dump import LastDump


def _extract_refunds_info(Iterable: Refund):
    pass


def _get_data_to_dump(
        user: User,
        last_dump: LastRefundsDump,
        already_included: int=0
) -> ReadyRefunds:  # ??
    """ Get refunds to dump, except already included ones """
    token = user.wms_access_token
    data = wms.get_ready_refunds(token, last_dump.workplace_id)
    data = islice(data, already_included)
    return extract_refunds_info(data)


def dump_ready_refunds(user: User, today_state: TodayDump) -> int:
    """ Enqueue the task for dumping refunds """
    status = last_dump.status
    if status == 'enqueued':
        raise AlreadyProcessed()

    already_included = today_state.included

    wms_key = today_state.workplace_id
    refunds = _get_data_to_dump(user, wms_key, already_included)

    just_included = SheetsService.append(today_state.report_url, refunds)
    today_state.add_new(just_included)

    return just_included
