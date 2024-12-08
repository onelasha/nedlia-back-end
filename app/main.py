"""
Main application entry point.
"""
import asyncio
from fastapi import FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve

from app.core.events import lifespan
from app.core.config import get_settings
from app.api.v1.router import router as v1_router

# Create FastAPI application
app = FastAPI(
    title=get_settings().APP_NAME,
    version=get_settings().APP_VERSION,
    lifespan=lifespan
)

# Add routers
app.include_router(v1_router)

async def start_server(port: int = 8000):
    """Start the server with the given configuration."""
    config = Config()
    config.bind = [f"127.0.0.1:{port}"]
    config.use_reloader = False
    config.accesslog = "-"
    
    shutdown_event = asyncio.Event()
    
    server_task = asyncio.create_task(
        serve(app, config, shutdown_trigger=shutdown_event.wait),
        name=f"server-{port}"
    )
    
    return shutdown_event, server_task

def run_server(port: int = 8000, *, loop=None):
    """Run the server."""
    if loop is None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    shutdown_event = None
    server_task = None
    
    try:
        shutdown_event, server_task = loop.run_until_complete(start_server(port))
        loop.run_forever()
    except Exception as e:
        raise RuntimeError(f"Failed to start server: {str(e)}")
    finally:
        if shutdown_event:
            shutdown_event.set()
        if server_task:
            try:
                loop.run_until_complete(server_task)
            except (asyncio.CancelledError, RuntimeError):
                pass
        if loop is not None and loop.is_running():
            loop.stop()
        loop.close()

if __name__ == "__main__":
    run_server(get_settings().PORT)
