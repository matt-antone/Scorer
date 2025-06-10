// src/services/websocket.ts

class WebSocketService {
  private ws: WebSocket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  constructor(private url: string) { }

  connect() {
    this.ws = new WebSocket(this.url);
    this.setupEventHandlers();
  }

  private setupEventHandlers() {
    this.ws?.addEventListener("open", this.handleOpen);
    this.ws?.addEventListener("message", this.handleMessage);
    this.ws?.addEventListener("close", this.handleClose);
    this.ws?.addEventListener("error", this.handleError);
  }

  private handleOpen = () => {
    console.log("WebSocket connected");
    this.reconnectAttempts = 0;
  };

  private handleMessage = (event: MessageEvent) => {
    console.log("Message from server: ", event.data);
    // Here we will later add logic to pass the message to a central state manager
  };

  private handleClose = () => {
    console.log("WebSocket disconnected");
    this.reconnect();
  };

  private handleError = (error: Event) => {
    console.error("WebSocket error:", error);
    this.ws?.close(); // This will trigger the handleClose and reconnect logic
  };

  private reconnect = () => {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      console.log(`WebSocket attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
      setTimeout(() => this.connect(), 3000 * this.reconnectAttempts);
    } else {
      console.error("WebSocket max reconnect attempts reached.");
    }
  };

  sendMessage(type: string, data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(
        JSON.stringify({
          type,
          data,
          timestamp: new Date().toISOString(),
        })
      );
    } else {
      console.error("Cannot send message, WebSocket is not open.");
    }
  }
}

// Create a singleton instance
const webSocketService = new WebSocketService(`ws://${window.location.host.replace('3000', '5001')}`);

export default webSocketService; 