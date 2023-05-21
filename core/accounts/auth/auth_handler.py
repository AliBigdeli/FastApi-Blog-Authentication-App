import time
from typing import Dict
from core.config import settings
import jwt
from fastapi import status, HTTPException


def encode_access_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "token_type": "access",
        "exp": int(time.time() + settings.JWT_EXPIRATION),
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    # return token_response(token)
    return token


def decode_access_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if decoded_token.get("token_type") != "access":
            raise HTTPException(status_code=401, detail="Invalid Token")
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired Token")


def encode_refresh_jwt(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "token_type": "refresh",
        "exp": int(time.time() + settings.JWT_REFRESH_EXPIRATION),
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    # return token_response(token)
    return token


def decode_refresh_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if decoded_token.get("token_type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid Token")
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired Token")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid Token")


def encode_reset_token(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "token_type": "reset",
        "exp": int(time.time() + settings.JWT_EXPIRATION),
    }
    token = jwt.encode(
        payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )

    # return token_response(token)
    return token


def decode_reset_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        if decoded_token.get("token_type") != "reset":
            raise HTTPException(status_code=401, detail="Invalid Token")
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Expired Token")
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=401, detail="Invalid Token")
