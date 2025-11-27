from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import chat_routes, message_routes
from slowapi.errors import RateLimitExceeded
from utils.limiter import limiter,  rate_limit_exceeded_handler
from config.config import FRONTEND_URL

# Initialize FastAPI app
app = FastAPI()

# Set Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

origins= [
    FRONTEND_URL,
]

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

# Routes
app.include_router(chat_routes.router, prefix="/api/chat")
app.include_router(message_routes.router, prefix="/api/message")


    

