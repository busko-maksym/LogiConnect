from settings import SECRET_KEY
from fastapi import Depends, status, HTTPException
from fastapi.security import HTTPBearer
import jwt


class VerifyToken:
    def __init__(self, token):
        self.token = token

    def verify(self, secret_key, algorithm):
        try:
            decoded_token = jwt.decode(self.token, secret_key, algorithms=[algorithm])
            return decoded_token
        except jwt.exceptions.DecodeError:
            return {"status": False, "msg": "Invalid token"}


def verify_token(token: HTTPBearer = Depends(HTTPBearer())):
    decoded_token = VerifyToken(token.credentials).verify(SECRET_KEY, "HS256")
    if decoded_token.get("status"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token or authentication required",
        )
    return decoded_token


def decode_token(token):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return decoded_token


def jwt_en(payload): return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
