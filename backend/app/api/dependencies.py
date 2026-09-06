from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.api.auth import decode_access_token
from app.providers import get_data_provider

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exc
    payload = decode_access_token(token)
    if not payload:
        raise credentials_exc
    data = get_data_provider()
    user = data.get_user(payload.get("sub"))
    if not user:
        raise credentials_exc
    return user


def require_role(*roles: str):
    def _dep(user: dict = Depends(get_current_user)) -> dict:
        if user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {roles}",
            )
        return user
    return _dep
