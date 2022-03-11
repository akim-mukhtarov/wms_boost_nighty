from app import app
from app.db import get_db
from app.auth import get_current_user
from app.models import User, Workplace
from app.rpc import rpc_method
from app.workplace.errors import WorkplaceNotFound
from app.workplace.crud import get_workplace

from fastapi import Depends
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from jsonrpcserver import Result, Success, Error

from . import schemas
from .crud import get_last_refunds_dump
from .errors import wrap_exception
from .today_dump import today_dump


@app.get(
    '/workplace/{workplace_id}/today_refunds_dump',
    response_model=schemas.RefundsDump)
def get_last_dump(
        workplace_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    workplace = get_workplace(db, workplace_id)
    return TodayDump(workplace)


@rpc_method
def dump_refunds(user: User, workplace_id: int) -> Result:
    """ Create and enqueue a task for dumping refunds
        If no refunds to dump, raise an Exception
        To check an execution progress,
            - connect to `workplace_updates` via websocket
            - or query `today_refunds_dump` by yourself """
    db = next(iter(get_db()))

    try:
        workplace = get_workplace(db, workplace_id)
        today_state = TodayDump(workplace)
        included = dump_ready_refunds(user, today_state)

    except Exception as e:
        return wrap_exception(e)

    return Success(included)
