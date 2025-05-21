import os

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_api_key(api_key: str = Security(api_key_header)):
    valid_api_keys_str = os.getenv("VALID_API_KEYS")
    if not valid_api_keys_str:
        raise HTTPException(
            status_code=500,
            detail="Server misconfiguration: VALID_API_KEYS not set",
        )

    valid_api_keys = valid_api_keys_str.split(",")

    if api_key not in valid_api_keys:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return api_key
