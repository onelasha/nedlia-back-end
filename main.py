from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import uvloop
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    print("Starting up...")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

def doSomething(arg: int) -> None:
    print("hello trg_21.11")

def hello_world() -> None:
    print("hello world")

@app.get("/hello")
async def hello():
    return {"message": "Hello World"}

async def start_server():
    config = Config()
    config.bind = ["0.0.0.0:80"]
    config.use_reloader = True
    config.worker_class = "uvloop"
    config.accesslog = "-"    
    await serve(app, config)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(start_server())
