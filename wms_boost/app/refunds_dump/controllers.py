from app import app
from app.db import get_db
from app.auth import get_current_user
from app.models import User, Workplace
from app.rpc import rpc_method
from app.workplace.errors import WorkplaceNotFound

from fastapi import Depends
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from jsonrpcserver import Result, Success, Error

from . import schemas
from .crud import get_last_refunds_dump
from .errors import wrap_exception


@app.get(
    '/workplace/{workplace_id}/last_refunds_dump',
    response_model=schemas.LastDumpState)
def get_last_dump(
        workplace_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    workplace = db.query(Workplace).get(workplace_id)
    if not workpalce:
        raise WorkplaceNotFound()
    return workplace.last_refunds_dump


@rpc_method
def dump_refunds(user: User, workplace_id: int) -> Result:
    """ Create and enqueue a task for dumping refunds
        If no refunds to dump, raise an Exception
        To check an execution progress,
            - connect to `workplace_updates` via websocket
            - or query `last_refunds_dump` by yourself """
    db = next(iter(get_db()))

    try:
        last_dump = get_last_refunds_dump(db, workplace_id)
        included = dump_ready_refunds(user, last_refunds_dump)
        
    except Exception as e:
        return wrap_exception(e)

    else:
        db.add(last_dump)
        db.commit()
        return Success(included)
