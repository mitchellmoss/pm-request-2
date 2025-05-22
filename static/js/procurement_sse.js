class ProcurementSSEClient {
  constructor(options = {}) {
    this.endpoint = options.endpoint || '/stream';
    this.reconnectDelay = options.reconnectDelay || 1000;
    this.maxReconnectDelay = options.maxReconnectDelay || 30000;
    this.handlers = {};
    this.reconnectAttempt = 0;
    this.eventSource = null;
    this.isConnected = false;
    this.setupVisibilityDetection();
    this.connect();
  }

  on(event, handler) {
    this.handlers[event] = handler;
  }

  connect() {
    if (this.eventSource) {
      this.eventSource.close();
    }
    try {
      this.eventSource = new EventSource(this.endpoint);
      this.eventSource.onopen = () => {
        this.isConnected = true;
        this.reconnectAttempt = 0;
      };
      this.eventSource.onmessage = (event) => {
        if (event.data.startsWith(': heartbeat')) {
          return;
        }
        const handler = this.handlers['message'];
        if (handler) {
          try {
            handler(JSON.parse(event.data));
          } catch (err) {
            console.error('Failed to parse SSE data', err);
          }
        }
      };
      this.eventSource.onerror = () => {
        this.isConnected = false;
        this.eventSource.close();
        this.scheduleReconnect();
      };
    } catch (err) {
      console.error('Failed to connect to SSE:', err);
      this.scheduleReconnect();
    }
  }

  scheduleReconnect() {
    const delay = Math.min(this.reconnectDelay * Math.pow(2, this.reconnectAttempt++), this.maxReconnectDelay);
    setTimeout(() => this.connect(), delay);
  }

  disconnect() {
    if (this.eventSource) {
      this.eventSource.close();
      this.eventSource = null;
    }
    this.isConnected = false;
  }

  setupVisibilityDetection() {
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) {
        this.disconnect();
      } else if (!this.isConnected) {
        this.connect();
      }
    });
  }
}
