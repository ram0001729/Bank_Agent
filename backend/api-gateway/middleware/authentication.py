from fastapi import Header, HTTPException, Security
from fastapi.security import APIKeyHeader

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_current_user(x_api_key: str = Header(None)):
    # Simple dev/demo auth dependency
    if x_api_key and x_api_key.startswith("admin"):
        return {"user": "admin", "role": "administrator"}
    elif x_api_key and x_api_key.startswith("employee"):
        return {"user": "bank_employee", "role": "employee"}
    return {"user": "customer_demo", "role": "customer"}
