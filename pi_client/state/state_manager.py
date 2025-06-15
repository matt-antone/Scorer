from typing import Any, Callable, List, Optional

class StateManager:
    def __init__(self, websocket_client):
        self.websocket_client = websocket_client
        self.observers: List[Callable[[dict], None]] = []
        self.state: Optional[dict] = None

    async def connect(self, url: str) -> None:
        try:
            await self.websocket_client.connect(url)
        except Exception as e:
            raise Exception(str(e))

    def is_connected(self) -> bool:
        return self.websocket_client.is_connected()

    async def send_state_update(self, state_update: dict) -> None:
        if not self._validate_state(state_update):
            raise ValueError('Invalid state')
        try:
            await self.websocket_client.send_message({'type': 'state_update', 'data': state_update})
        except Exception as e:
            raise Exception(str(e))

    def register_observer(self, observer: Callable[[dict], None]) -> None:
        if observer not in self.observers:
            self.observers.append(observer)

    def remove_observer(self, observer: Callable[[dict], None]) -> None:
        if observer in self.observers:
            self.observers.remove(observer)

    async def _on_state_update(self, state_update: dict) -> None:
        self.state = state_update
        for observer in self.observers:
            observer(state_update)

    def _validate_state(self, state: Any) -> bool:
        return isinstance(state, dict) and state is not None 