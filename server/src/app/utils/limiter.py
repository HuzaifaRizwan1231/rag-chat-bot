from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request, status
from fastapi.responses import JSONResponse
from utils.response_builder import ResponseBuilder

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)

def rate_limit_exceeded_handler(request: Request, exc):
    response = ResponseBuilder().setSuccess(False).setMessage("Rate Limit Exceeded").setStatusCode(status.HTTP_429_TOO_MANY_REQUESTS).setError("Rate Limit has been exceeded").build()
    return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content=response)
