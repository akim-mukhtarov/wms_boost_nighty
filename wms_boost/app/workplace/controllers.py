from typing import Dict, Optional

from app import app
from app.db import get_db
from app.auth import get_current_user
from app.auth.security import raw_decode
from app.models import User
from app.models import Workplace as DbWorkplace
from app.rpc import rpc_method

from fastapi import Depends, WebSocket, status
from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session
from jsonrpcserver import Result, Success, Error

from .crud import init_workplace as init_db_workplace
from .crud import get_workplace
from .workplace_observer import WorkplaceObserver
from . import schemas
from .workplace import Workplace


@rpc_method
def init_workplace(data: schemas.WorkplaceCreate) -> Result:
    """  Initialize `Workplace` and linked resources:
            `LastRefundsDump` and `StorageStepsProgress` """
    db = next(iter(get_db()))

    db_workplace = db.query(DbWorkplace).get(data.wms_key)
    if db_workplace:
        return Error(6, "Workplace with provided wms_key already exists")

    db.add_all(init_db_workplace(data))
    db.commit()
    return Success()


@app.get('/workplace/{workplace_id}', response_model=schemas.WorkplaceModel)
def get_workplace(
        workplace_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    db_workplace = get_workplace(db, workplace_id)
    return Workplace(db_workplace)

# helper
async def auth_connection(ws: WebSocket) -> bool:
    await ws.accept()
    token = await ws.receive_text()
    payload = raw_decode(token)
    return bool(payload)


@app.websocket("/ws/workplace/{workplace_id}/updates")
async def workplace_updates(ws: WebSocket, workplace_id: int):
    """ Check updates on workplace and
        its related resources and return json """

    if not await auth_connection(ws):
        await ws.close(code=status.WS_1008_POLICY_VIOLATION)
    # TODO: consider rewrite with async context manager
    observer = WorkplaceObserver(workplace_id)\
            .on_update(ws.send_json)\
            .check_alive(lambda: ws.client_state.name == "CONNECTED")

    await observer.observe()
    await ws.close()    # ??
