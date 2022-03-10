import pydantic


class RefundsDump(pydantic.BaseModel):
    report_url: str
    included: int
    processed: int
    status: str

    class Config:
        orm_mode=True
