from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.utils import decode_token
# from models import RoleEnum

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = await decode_token(refresh_token=token, expected_type="access")
    return payload
