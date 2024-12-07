from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve
import asyncio
import uvloop  # Add this import


app = FastAPI()

def doSomething(arg: int) -> None:
    print("hello trg_21.11")

def hello_world() -> None:
    print("hello world")

async def start_server():
    config = Config()
    config.bind = ["0.0.0.0:80"]
    config.use_reloader = True
    # config.debug = True
    config.worker_class = "uvloop"
    config.accesslog = "-"    
    await serve(app, config)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())  # Add this line
    asyncio.run(start_server())
