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

@pytest.mark.asyncio
async def test_run_server():
    # Create a mock event loop
    class MockEventLoop:
        def __init__(self):
            self.closed = False
            self.is_running_flag = False
            
        def run_until_complete(self, coro):
            return (asyncio.Event(), asyncio.create_task(asyncio.sleep(0)))
            
        def run_forever(self):
            self.is_running_flag = True
            
        def close(self):
            self.closed = True
            
        def is_running(self):
            return self.is_running_flag
            
        def stop(self):
            self.is_running_flag = False
    
    # Create our mock loop
    mock_loop = MockEventLoop()
    
    try:
        # Run the server with our mock loop
        test_port = find_free_port()
        run_server(port=test_port, loop=mock_loop)
        
        # Verify the loop was properly used
        assert mock_loop.closed, "Loop should be closed after server run"
        
    except Exception as e:
        pytest.fail(f"Test failed: {str(e)}")

@pytest.mark.asyncio
async def test_run_server_error_handling():
    # Create a mock event loop that raises an error
    class MockEventLoop:
        def __init__(self):
            self.closed = False
            self.is_running_flag = False
            
        def run_until_complete(self, coro):
            raise RuntimeError("Mock error")
            
        def run_forever(self):
            self.is_running_flag = True
            
        def close(self):
            self.closed = True
            
        def is_running(self):
            return self.is_running_flag
            
        def stop(self):
            self.is_running_flag = False
    
    # Create our mock loop
    mock_loop = MockEventLoop()
    
    # Run the server with our mock loop and expect an error
    test_port = find_free_port()
    with pytest.raises(RuntimeError) as exc_info:
        run_server(port=test_port, loop=mock_loop)
    
    # Verify the error message
    assert "Failed to start server: Mock error" in str(exc_info.value)
    # Verify the loop was properly closed
    assert mock_loop.closed, "Loop should be closed even after error"
