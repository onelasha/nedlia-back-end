import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from main import doSomething, hello_world, app, start_server, run_server
import io
import sys
import asyncio
import socket
from contextlib import closing

def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
        return port

def test_do_something(test_client: TestClient):
    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    doSomething(0)
    
    # Reset stdout
    sys.stdout = sys.__stdout__
    assert "hello trg_21.11" in captured_output.getvalue()

def test_hello_world(test_client: TestClient):
    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    hello_world()
    
    # Reset stdout
    sys.stdout = sys.__stdout__
    assert "hello world" in captured_output.getvalue()

def test_hello_endpoint(test_client: TestClient):
    response = test_client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_hello_response_type(test_client: TestClient):
    response = test_client.get("/hello")
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data

@pytest.mark.asyncio(loop_scope="function")
async def test_lifespan():
    # Capture stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output

    # Test the lifespan using TestClient which properly handles the lifespan context
    with TestClient(app) as client:
        response = client.get("/hello")
        assert response.status_code == 200
    
    # Reset stdout
    sys.stdout = sys.__stdout__
    output = captured_output.getvalue()
    
    # Check if startup and shutdown messages were logged
    assert "Starting up..." in output
    assert "Shutting down..." in output

@pytest.mark.asyncio(loop_scope="function")
async def test_start_server():
    # Find a free port
    test_port = find_free_port()
    
    # Start the server with a timeout
    try:
        shutdown_event, server_task = await asyncio.wait_for(
            start_server(port=test_port),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        pytest.fail("Server startup timed out")
        return
    
    try:
        # Give the server a moment to start
        await asyncio.sleep(0.1)
        
        # Make a test request with timeout
        async with AsyncClient(base_url=f"http://127.0.0.1:{test_port}") as client:
            try:
                response = await asyncio.wait_for(
                    client.get("/hello"),
                    timeout=2.0
                )
                assert response.status_code == 200
            except asyncio.TimeoutError:
                pytest.fail("Request timed out")
            except Exception as e:
                pytest.fail(f"Request failed: {str(e)}")
    finally:
        # Cleanup with timeout
        shutdown_event.set()
        try:
            await asyncio.wait_for(server_task, timeout=2.0)
        except asyncio.TimeoutError:
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

@pytest.mark.asyncio(loop_scope="function")
async def test_run_server():
    # Create a future to run the server
    loop = asyncio.get_event_loop()
    server_future = loop.create_future()
    
    def mock_run_until_complete(coro):
        async def mock_start_server(port=8000):
            return asyncio.Event(), asyncio.create_task(asyncio.sleep(0))
        if asyncio.iscoroutine(coro):
            return loop.run_until_complete(mock_start_server())
        return coro
    
    # Mock the event loop
    loop.run_until_complete = mock_run_until_complete
    
    # Run the server in a separate task
    server_task = asyncio.create_task(
        asyncio.to_thread(run_server, port=8000)
    )
    
    # Give it a moment to start
    await asyncio.sleep(0.1)
    
    # Cancel the task
    server_task.cancel()
    try:
        await server_task
    except asyncio.CancelledError:
        pass  # Expected
