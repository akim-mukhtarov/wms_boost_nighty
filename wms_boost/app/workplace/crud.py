from app.models import (
    Workplace,
    RefundsDumpSettings,
    StorageStepsSettings
)
from sqlalchemy.orm import Session

from .errors import WorkplaceNotFound
from .schemas import WorkplaceCreate


def init_workplace(data: WorkplaceCreate):

    workplace = Workplace(
        wms_key = data.wms_key,
        short_name = data.short_name,
        timezone = data.timezone)

    refunds_dump_settings = RefundsDumpSettings(
        workplace_id = data.wms_key,
        report_url = data.reports_urls.refunds_dump,
        redis_key = RefundsDumpSettings.generate_redis_key(workplace_id))

    storage_steps_settings = StorageStepsSettings(
        workplace_id = data.wms_key,
        report_url = data.reports_urls.storage_steps,
        redis_key = StorageStepsSettings.generate_redis_key(workplace_id))

    return workplace, refunds_dump_settings, storage_steps_settings


def get_workplace(db: Session, workplace_id: int) -> Workplace:
    workplace = db.query(Workplace).get(workplace_id)
    if not workplace:
        raise WorkplaceNotFound()
    return workplace
