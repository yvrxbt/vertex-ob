from collections import defaultdict
from datetime import datetime
from decimal import Decimal
import sys
from src.utils.logger import Logger
from typing import Dict

class OrderBook:
    def __init__(self):
        self.asks: Dict[Decimal, Decimal] = defaultdict(Decimal)
        self.min_ask_price: Decimal = Decimal(float("inf"))
        self.bids: Dict[Decimal, Decimal] = defaultdict(Decimal)
        self.max_bid_price: Decimal = Decimal(0)
        self._max_depth = 100
        self.logger = Logger.setup_logger("orderbook")
        self.last_state_log = datetime.now()
        self.state_log_interval = 60  # Log state every 60 seconds

    # Main callback function that occurs on every message from the WebSocket feed.
    async def update(self, data: dict):
        """
        Process orderbook updates from WebSocket. 
        Data is in the format of:
        {
            "type":"book_depth",
            // book depth aggregates a number of events once every 50ms
            // these are the minimum and maximum timestamps from 
            // events that contributed to this response
            "min_timestamp": "1683805381879572835",
            "max_timestamp": "1683805381879572835",
            // the max_timestamp of the last book_depth event for this product
            "last_max_timestamp": "1683805381771464799",
            "product_id":1,
            // changes to the bid side of the book in the form of [[price, new_qty]]
            "bids":[["21594490000000000000000","51007390115411548"]],
            // changes to the ask side of the book in the form of [[price, new_qty]]
            "asks":[["21694490000000000000000","0"],["21695050000000000000000","0"]]
        }
        from https://docs.vertexprotocol.com/developer-resources/api/subscriptions/events#book-depth.
        
        Some optimizations made:
        - Using ints since we get ints anyways, and it's faster than floats/Decimals, and we keep precision.
        """
        msg_type = data.get("type", None)
        if not msg_type or msg_type != "book_depth":
            return

        try:
            # Get references to avoid dict lookups in loops
            asks = data.get("asks", [])
            bids = data.get("bids", [])
            asks_dict = self.asks
            bids_dict = self.bids
            
            # Process asks
            if asks:  # Only enter if there are asks to process
                for price_str, qty_str in asks:
                    # Direct int conversion, no float intermediary
                    price = int(price_str)
                    qty = int(qty_str)
                    
                    if qty == 0:
                        asks_dict.pop(price, None)
                    else:
                        asks_dict[price] = qty
                
                # Update min_ask_price only once after all updates
                if asks_dict:
                    self.min_ask_price = min(asks_dict.keys())
                else:
                    self.min_ask_price = sys.maxsize

            # Process bids
            if bids:  # Only enter if there are bids to process
                for price_str, qty_str in bids:
                    price = int(price_str)
                    qty = int(qty_str)
                    
                    if qty == 0:
                        bids_dict.pop(price, None)
                    else:
                        bids_dict[price] = qty
                
                # Update max_bid_price only once after all updates
                if bids_dict:
                    self.max_bid_price = max(bids_dict.keys())
                else:
                    self.max_bid_price = 0

        except Exception as e:
            self.logger.error(f"Error updating orderbook: {str(e)}")