import pytz
from typing import List, Optional
from pydantic import BaseModel, validator


class WorkplaceBase(BaseModel):
    wms_key: int
    short_name: str
    timezone: str

    class Config:
        orm_mode = True


class ReportsUrls(BaseModel):

    refunds_dump: str
    storage_steps: str

    @validator("refunds_dump", "storage_steps")
    def validate_spreadsheet_url(cls, url: str):
        prefix = 'https://docs.google.com/spreadsheets/d/'
        if not url.startswith(prefix):
            raise ValueError(
                'Valid spreadsheets url starts with %' % prefix)
        return url


class WorkplaceCreate(WorkplaceBase):

    reports_urls: ReportsUrls

    @validator("timezone")
    def validate_timezone(cls, tz: str):
        if not tz in pytz.common_timezones_set:
            raise ValueError(
                'Valid timezone must be one of the'
                'listed in Olson tz database')
        return tz


class Workplace(WorkplaceBase):

    class ResourceWithReport(BaseModel):
        report_url: str

        class Config:
            orm_mode = True

    last_refunds_dump: ResourceWithReport
    storage_steps_progress: ResourceWithReport

    class Config:
        orm_mode = True
