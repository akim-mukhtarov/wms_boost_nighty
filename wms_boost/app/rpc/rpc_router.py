from app import app
from app.models import User
from app.auth import get_current_user

from fastapi import Request, Response, Depends
from jsonrpcserver import dispatch


@app.post("/")
async def private_rpc_router(
        request: Request,
        user: User = Depends(get_current_user)
):
    return Response(dispatch(await request.body(), context = user))
