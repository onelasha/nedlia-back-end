from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import uvloop
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    
    shutdown_event = asyncio.Event()
    await serve(app, config, shutdown_trigger=shutdown_event.wait)
    return shutdown_event

def run_server():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(start_server())
    finally:
        loop.close()

if __name__ == "__main__":
    run_server()
