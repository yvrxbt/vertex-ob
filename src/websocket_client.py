import asyncio
import json
import websockets

from src.utils.logger import Logger
from typing import Callable, Optional
from websockets.exceptions import ConnectionClosed

class VertexWebsocketClient:
    def __init__(self, callback: Callable, product_id: int, product_name: str):
        self.url = "wss://gateway.prod.vertexprotocol.com/v1/subscribe"
        self.callback = callback
        self.product_id = product_id
        self.product_name = product_name
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.is_connected = False
        self.logger = Logger.setup_logger("websocket")
        
        # Retry/backoff parameters
        self.max_retries = 5
        self.initial_backoff = 1.0
        self.max_backoff = 60.0
        self.backoff_factor = 2
        
    async def connect(self):
        retry_count = 0
        current_backoff = self.initial_backoff

        while True:
            try:
                # Websockets library automatically handles pings.
                async with websockets.connect(self.url) as websocket:
                    self.ws = websocket
                    self.is_connected = True
                    self.logger.info("Connected to Vertex WebSocket")
                    # Reset reconnection parameters on successful connection
                    retry_count = 0
                    current_backoff = self.initial_backoff
                    
                    # Subscribe to product orderbook
                    self.logger.info(f"Subscribing to {self.product_name} orderbook")
                    subscribe_message = {
                        "method": "subscribe",
                        "stream": {
                            "type": "book_depth",
                            "product_id": self.product_id
                        },
                        "id": 10
                    }
                    await websocket.send(json.dumps(subscribe_message))
                    
                    while True:
                        message = await websocket.recv()
                        await self.handle_message(message)

            except (ConnectionClosed, Exception) as e:
                self.is_connected = False
                retry_count += 1
                
                if retry_count > self.max_retries:
                    self.logger.error(f"Maximum retry attempts ({self.max_retries}) reached. Stopping reconnection.")
                    raise Exception("Max retry attempts reached")
                
                self.logger.error(f"WebSocket error: {str(e)}. Attempt {retry_count}/{self.max_retries}")
                self.logger.info(f"Reconnecting in {current_backoff} seconds...")
                
                await asyncio.sleep(current_backoff)
                # Exponential backoff with maximum limit
                current_backoff = min(current_backoff * self.backoff_factor, self.max_backoff)

    async def handle_message(self, message: str):
        """Process incoming WebSocket messages"""
        try:
            data = json.loads(message)
            await self.callback(data)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to decode message: {message}")
        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")