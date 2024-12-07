from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import uvloop
from contextlib import asynccontextmanager
import signal

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

async def start_server(port: int = 8000):
    config = Config()
    config.bind = [f"127.0.0.1:{port}"]
    config.use_reloader = False  # Disable reloader for testing
    config.worker_class = "uvloop"
    config.accesslog = "-"
    
    shutdown_event = asyncio.Event()
    
    server_task = asyncio.create_task(
        serve(app, config, shutdown_trigger=shutdown_event.wait),
        name=f"server-{port}"
    )
    
    # Return both the shutdown event and task for better control
    return shutdown_event, server_task

def run_server(port: int = 8000):
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        shutdown_event, server_task = loop.run_until_complete(start_server(port))
        loop.run_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        shutdown_event.set()
        loop.run_until_complete(server_task)
        loop.close()

if __name__ == "__main__":
    run_server()
