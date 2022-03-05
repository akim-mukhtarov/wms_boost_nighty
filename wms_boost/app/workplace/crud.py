from app.models import Workplace, LastRefundsDump, StorageStepsProgress

from .schemas import WorkplaceCreate


def init_workplace(data: WorkplaceCreate):

    workplace = Workplace(
        wms_key = data.wms_key,
        short_name = data.short_name,
        timezone = data.timezone)

    refunds_dump = LastRefundsDump(
        workplace_id = data.wms_key,
        report_url = data.reports_urls.refunds_dump)

    storage_steps = StorageStepsProgress(
        workplace_id = data.wms_key,
        report_url = data.reports_urls.storage_steps)

    return workplace, refunds_dump, storage_steps
