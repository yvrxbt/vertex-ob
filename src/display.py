import asyncio
import os

class OrderBookDisplay:
    def __init__(self, orderbook, product_name: str, update_frequency: float, display_rows: int):
        self.orderbook = orderbook
        self.product_name = product_name
        self.update_frequency = update_frequency
        self.display_rows = display_rows
        self.display_decimals = 10**18
        
        # Pre-compute static strings
        self._empty_row = " " * 40
        self._separator = "=" * 65
        self._header = f"\n{self._separator}\n{self.product_name} {'Orderbook':^65}\n{self._separator}"
        self._col_headers = f"{'Price':>12} {'Quantity':>12} {'Total ($)':>15}"
        self._dash_line = "-" * 65
        
        # ANSI color codes
        self._red = "\033[91m"
        self._green = "\033[92m"
        self._reset = "\033[0m"
        
        # Pre-format strings
        self._price_fmt = "{:>12.2f}"
        self._qty_fmt = "{:>12.6f}"
        self._total_fmt = "{:>15.2f}"
    
    async def display_loop(self):
        """Continuously update the orderbook display"""
        try:
            while True:
                self._print_orderbook()
                await asyncio.sleep(self.update_frequency)
                
        except asyncio.CancelledError:
            # Clear the screen one last time when shutting down
            os.system('cls' if os.name == 'nt' else 'clear')
            raise
            
        except Exception as e:
            print(f"Error in display loop: {str(e)}")
            raise
        
    def _format_decimal(self, value: int) -> float:
        """Convert raw value to human readable format"""
        return value / self.display_decimals

    def _format_order_line(self, price: float, qty: float, color: str) -> str:
        """Format a single order book line with pre-computed formats"""
        total = price * qty
        return f"{color}{self._price_fmt.format(price)} {self._qty_fmt.format(qty)} {self._total_fmt.format(total)}{self._reset}"

    def _format_spread_line(self, lowest_ask: float, highest_bid: float) -> str:
        """Format the spread information line"""
        spread = lowest_ask - highest_bid
        spread_pct = (spread / lowest_ask) * 100
        mid_price = (lowest_ask + highest_bid) / 2
        
        mid_text = f"Mid: ${mid_price:.2f}"
        spread_text = f"Spread: ${spread:.2f} ({spread_pct:.2f}%)"
        padding = 65 - len(mid_text) - len(spread_text)
        
        return f"\n{mid_text}{' ' * padding}{spread_text}\n"

    def _print_orderbook(self):
        """Print current orderbook state to terminal"""
        # Clear screen and print static headers
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self._header)
        print(self._col_headers)
        print(self._dash_line)

        # Get and sort orders once
        asks = sorted(self.orderbook.asks.items())[:self.display_rows]
        bids = sorted(self.orderbook.bids.items(), reverse=True)[:self.display_rows]
        
        # Print asks (bottom to top)
        for i in range(self.display_rows):
            idx = self.display_rows - i - 1
            if idx < len(asks):
                price, qty = asks[idx]
                price_f = self._format_decimal(price)
                qty_f = self._format_decimal(qty)
                print(self._format_order_line(price_f, qty_f, self._red))
            else:
                print(f"{self._red}{self._empty_row}{self._reset}")

        # Print spread information
        if asks and bids:
            lowest_ask = self._format_decimal(asks[0][0])
            highest_bid = self._format_decimal(bids[0][0])
            
            if highest_bid >= lowest_ask:
                warning = "*** CROSSED MARKETS ***"
                padding = (65 - len(warning)) // 2
                print(f"\n{' ' * padding}{warning}\n")
            else:
                print(self._format_spread_line(lowest_ask, highest_bid))

        # Print bids (top to bottom)
        for i in range(self.display_rows):
            if i < len(bids):
                price, qty = bids[i]
                price_f = self._format_decimal(price)
                qty_f = self._format_decimal(qty)
                print(self._format_order_line(price_f, qty_f, self._green))
            else:
                print(f"{self._green}{self._empty_row}{self._reset}")

        print("\n")