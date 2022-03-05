from app import app
from app.db import get_db
from app.wms_api import WmsApi as wms
from app.wms_api import AuthenticationError, WmsServerError, UnexpectedApiResponse
from app.wms_api.models import AuthResult

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .schemas import Tokens
from .crud import get_or_create_user
from .security import create_tokens


def authenticate(creds) -> AuthResult:
    try:
        return wms.authenticate(creds.username, creds.password)
    except UnexpectedApiResponse:
        raise HTTPException(501)
    except WmsServerError:
        raise HTTPException(523)
    except AuthenticationError:
        rause HTTPException(403)


@app.post('/auth/token', response_model=Tokens)
def emit_tokens(
        creds: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):

    auth_result = authenticate(creds).user_info
    user_info = auth_result.user_info
    user = get_or_create_user(db, user_info)

    user.update_tokens(
        auth_result.access_token,
        auth_result.refresh_token)

    db.add(user)
    db.commit()

    access, refresh = create_tokens(user)

    return {
        'access_token': access,
        'refresh_token': refresh
    }
