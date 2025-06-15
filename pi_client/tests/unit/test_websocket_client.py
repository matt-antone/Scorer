import pytest
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from pi_client.state.websocket_client import WebSocketClient

@pytest.fixture
def websocket_client():
    return WebSocketClient()

@pytest.fixture
def mock_websocket():
    mock = AsyncMock()
    mock.send = AsyncMock()
    mock.recv = AsyncMock()
    mock.close = AsyncMock()
    mock.closed = False
    return mock

@pytest.mark.asyncio
async def test_connect_success(websocket_client, mock_websocket):
    with patch('websockets.connect', new_callable=AsyncMock, return_value=mock_websocket):
        await websocket_client.connect('ws://localhost:8765')
        assert websocket_client.connection is not None
        assert websocket_client.is_connected()

@pytest.mark.asyncio
async def test_connect_failure(websocket_client):
    with patch('websockets.connect', new_callable=AsyncMock, side_effect=Exception('Connection failed')):
        with pytest.raises(Exception) as exc_info:
            await websocket_client.connect('ws://localhost:8765')
        assert str(exc_info.value) == 'Connection failed: Connection failed'
        assert not websocket_client.is_connected()

@pytest.mark.asyncio
async def test_send_message_success(websocket_client, mock_websocket):
    websocket_client.connection = mock_websocket
    message = {'type': 'test', 'data': 'test_data'}
    await websocket_client.send_message(message)
    mock_websocket.send.assert_called_once_with(json.dumps(message))

@pytest.mark.asyncio
async def test_send_message_not_connected(websocket_client):
    with pytest.raises(RuntimeError) as exc_info:
        await websocket_client.send_message({'type': 'test'})
    assert str(exc_info.value) == 'Not connected to server'

@pytest.mark.asyncio
async def test_receive_message(websocket_client, mock_websocket):
    websocket_client.connection = mock_websocket
    test_message = {'type': 'test', 'data': 'test_data'}
    mock_websocket.recv.return_value = json.dumps(test_message)
    
    message = await websocket_client.receive_message()
    assert message == test_message
    mock_websocket.recv.assert_called_once()

@pytest.mark.asyncio
async def test_close_connection(websocket_client, mock_websocket):
    websocket_client.connection = mock_websocket
    await websocket_client.close()
    mock_websocket.close.assert_called_once()
    assert not websocket_client.is_connected()

@pytest.mark.asyncio
async def test_message_handler_registration(websocket_client):
    handler = AsyncMock()
    websocket_client.register_handler('test_type', handler)
    assert 'test_type' in websocket_client.handlers
    assert websocket_client.handlers['test_type'] == handler

@pytest.mark.asyncio
async def test_message_handling(websocket_client, mock_websocket):
    handler = AsyncMock()
    websocket_client.connection = mock_websocket
    websocket_client.register_handler('test_type', handler)
    
    test_message = {'type': 'test_type', 'data': 'test_data'}
    mock_websocket.recv.return_value = json.dumps(test_message)
    
    # Set up the mock to raise an exception after first call to stop the loop
    mock_websocket.recv.side_effect = [
        json.dumps(test_message),
        Exception('Stop loop')
    ]
    
    # Run handle_messages
    websocket_client._running = True
    with pytest.raises(Exception) as exc_info:
        await websocket_client.handle_messages()
    assert str(exc_info.value) == 'Stop loop'
    
    # Verify handler was called correctly
    handler.assert_called_once_with(test_message['data'])

@pytest.mark.asyncio
async def test_reconnection(websocket_client, mock_websocket):
    with patch('websockets.connect', new_callable=AsyncMock, return_value=mock_websocket) as mock_connect:
        await websocket_client.connect('ws://localhost:8765')
        mock_websocket.closed = True
        
        with pytest.raises(Exception) as exc_info:
            await websocket_client.ensure_connection()
        assert str(exc_info.value) == 'Connection lost' 