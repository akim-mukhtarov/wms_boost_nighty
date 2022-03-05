from app.models import User
from app.wms_api.models import AuthResult
from sqlalchemy.orm import Session


def get_or_create_user(db: Session, user_info: AuthResult.UserInfo) -> User:
    user = db.query(User).get(user_info.id)
    if not user:
        user = User(
            id = user_info.id,
            first_name=user_info.first_name,
            last_name=user_info.last_name)
    return user
