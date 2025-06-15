import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from pi_client.state.state_manager import StateManager

@pytest.fixture
def mock_websocket_client():
    mock = AsyncMock()
    mock.is_connected.return_value = True
    return mock

@pytest.fixture
def state_manager(mock_websocket_client):
    return StateManager(websocket_client=mock_websocket_client)

@pytest.mark.asyncio
async def test_connect_success(state_manager, mock_websocket_client):
    await state_manager.connect('ws://localhost:8765')
    mock_websocket_client.connect.assert_awaited_once_with('ws://localhost:8765')
    assert state_manager.is_connected()

@pytest.mark.asyncio
async def test_connect_failure(state_manager, mock_websocket_client):
    mock_websocket_client.connect.side_effect = Exception('Connection failed')
    with pytest.raises(Exception) as exc_info:
        await state_manager.connect('ws://localhost:8765')
    assert str(exc_info.value) == 'Connection failed'

@pytest.mark.asyncio
async def test_send_state_update(state_manager, mock_websocket_client):
    state_update = {'score': 42}
    await state_manager.send_state_update(state_update)
    mock_websocket_client.send_message.assert_awaited_once_with({'type': 'state_update', 'data': state_update})

@pytest.mark.asyncio
async def test_receive_state_update_notifies_observers(state_manager, mock_websocket_client):
    observer = MagicMock()
    state_manager.register_observer(observer)
    state_update = {'score': 99}
    await state_manager._on_state_update(state_update)
    observer.assert_called_once_with(state_update)

@pytest.mark.asyncio
async def test_observer_registration_and_removal(state_manager):
    observer = MagicMock()
    state_manager.register_observer(observer)
    assert observer in state_manager.observers
    state_manager.remove_observer(observer)
    assert observer not in state_manager.observers

@pytest.mark.asyncio
async def test_error_handling_on_send(state_manager, mock_websocket_client):
    mock_websocket_client.send_message.side_effect = Exception('Send failed')
    with pytest.raises(Exception) as exc_info:
        await state_manager.send_state_update({'foo': 'bar'})
    assert str(exc_info.value) == 'Send failed'

@pytest.mark.asyncio
async def test_state_validation(state_manager):
    # Accept valid state
    valid_state = {'score': 10}
    assert state_manager._validate_state(valid_state)
    # Reject invalid state
    invalid_state = None
    assert not state_manager._validate_state(invalid_state) 