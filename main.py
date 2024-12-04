import asyncio

from src.websocket_client import VertexWebsocketClient
from src.orderbook import OrderBook
from src.display import OrderBookDisplay
from src.utils.logger import Logger

async def main():
    # Initialize logger
    logger = Logger.setup_logger("main")
    logger.info("Starting Vertex OrderBook application")
    
    # Initialize components
    update_frequency = 0.5 # Update display every 0.5 seconds
    product_name = "BTC-USDC"
    product_id = 2
    orderbook_depth = 10
    orderbook = OrderBook()
    client = VertexWebsocketClient(callback=orderbook.update, product_id=product_id, product_name=product_name)
    display = OrderBookDisplay(orderbook, product_name=product_name, update_frequency=update_frequency, display_rows=orderbook_depth)
    
     # Create tasks
    ws_task = asyncio.create_task(client.connect())
    display_task = asyncio.create_task(display.display_loop())
    
    try:
        logger.info("Application started successfully")
        await asyncio.gather(ws_task, display_task)
        
    except KeyboardInterrupt:
        logger.info("Shutdown initiated via keyboard interrupt")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        
    finally:
        # Cleanup tasks
        logger.info("Cleaning up tasks...")
        ws_task.cancel()
        display_task.cancel()
        await asyncio.gather(ws_task, display_task, return_exceptions=True)
        logger.info("Application shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")