from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_to_mongo, close_mongo_connection
from app.routes import auth, users, stats

@asynccontextmanager
async def lifespan(app: FastAPI):
    # at the begining of active server
    await connect_to_mongo()
    yield
    # at the closed server
    await close_mongo_connection()

# 1. create app FastAPI just once
app = FastAPI(
    title="Production User Management & Auth API",
    description="REST API by use FastAPI و MongoDB",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# 2. add setting CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. register Routers  with Prefix suitable
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(stats.router, prefix="/stats", tags=["Stats"])


@app.get("/")
def home():
    return {
        "status": "Online",
        "documentation": "/docs"
    }