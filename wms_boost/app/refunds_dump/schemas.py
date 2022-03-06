from app.models import LastRefundsDump as LastRefundsDumpModel
import pydantic


class LastRefundsDump(pydantic.BaseModel):
    report_url: str
    included: int
    processed: int

    date: Optional[datetime]
    status: LastRefundsDumpModel.status_choices

    class Config:
        orm_mode=True
