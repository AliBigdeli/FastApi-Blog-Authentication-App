from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .auth_handler import decode_access_jwt


class JWTBearer(HTTPBearer):
    '''
    In summary, if a user receives a 401 status code, it means they need to authenticate themselves first to access the resource. 
    If a user receives a 403 status code, it means they are authenticated, but they still do not have the necessary permissions to access the resource.
    '''

    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=401, detail="Invalid token or expired token.")
            return decode_access_jwt(credentials.credentials).get("user_id")
        else:
            raise HTTPException(
                status_code=401, detail="Not authenticated")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decode_access_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid
