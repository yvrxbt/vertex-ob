# Project Name: Websocket with Internal Orderbook

## Run Instructions

Using Python 3.10, install dependencies and run the application:
```bash
pip install -r requirements.txt
python main.py
```

It is recommended to run the application with a conda environment to avoid dependency issues. Please setup a conda environment,
install the requirements, and activate it before running the application with `python main.py`.

```bash
conda create -n vertex-ob python=3.10
conda activate vertex-ob
conda install -c conda-forge websockets asyncio
python main.py
```

Once you run it, the orderbook will be displayed in the terminal in the format of:

```
=================================================================
BTC-USDC Orderbook
=================================================================
       Price     Quantity       Total ($)
-----------------------------------------------------------------
    96079.00     0.016000         1537.26
    96077.00     0.078000         7494.01
    96076.00     0.016000         1537.22
    96075.00     0.240000        23058.00
    96074.00     0.024000         2305.78
    96071.00     0.020000         1921.42
    96069.00     0.095000         9126.56
    96066.00     0.020000         1921.32
    96065.00     0.062000         5956.03
    96059.00     0.194000        18635.45

Mid: $96058.50                              Spread: $1.00 (0.00%)

    96058.00     0.100000         9605.80
    96057.00     0.024000         2305.37
    96056.00     0.020000         1921.12
    96055.00     0.086000         8260.73
    96051.00     0.090000         8644.59
    96048.00     0.041000         3937.97
    96046.00     0.097000         9316.46
    96044.00     0.094000         9028.14
    96041.00     0.032000         3073.31
    96040.00     0.042000         4033.68
```
keeping 10 levels on each side.

## Code entry point
The main.py file is the entry point to the application. Running it will initialize the websocket client, orderbook, and display classes, and then create asyncio tasks for the websocket connection and the display loop.

The websocket connection is established using the VertexWebsocketClient class connecting to a pre-defined URL/subscription message, which is initialized with a callback function that updates the orderbook. The orderbook class is responsible for processing the messages from the websocket client and updating the internal representation of the orderbook. Finally, the display class is responsible for printing the orderbook to the terminal in a user-friendly format.
## Introduction

This project aims to develop a simple application in the language of your choice that streams a live orderbook for BTC-USDC from the on-chain perpetual exchange, Vertex. You'll need to recreate the orderbook using a stream of updates received from the exchange's public WebSocket. No API keys are required, but you will need a VPN to connect to the WebSocket if subscribing inside the United States. You may use any resources available, including AI tools like ChatGPT.

To pass this case study, you need to demonstrate the following:

## Must Complete

1. **WebSocket Client:** Implement a WebSocket client to communicate with Vertex and stream orderbook updates via the Book Depth stream.

2. **Orderbook Builder:** Develop a class to process and build the orderbook from the streamed updates.

3. **Entrypoint / Orderbook Display:** Provide an entry point to the application that displays the assembled orderbook *live* to the user. This can be printed to the terminal. The quality of the display is not the focus of the case study, however it will be used to verify correctness of your OB building approach.

## Implementation Details

### WebSocket Client

- Refer to the [Vertex documentation](https://docs.vertexprotocol.com/developer-resources/api/subscriptions/events#book-depth) for details on obtaining orderbook updates. You cannot use the Python SDK; implement everything from scratch.
- You can build a synchronous or asynchronous WebSocket client. If you choose synchronous, use threading and locks to handle race conditions. For asynchronous, ensure the entire app follows the async paradigm. Consistency is key.
- Focus on the BTC orderbook on the Arbitrum One blockchain:
  - `product_id: 2` (BTC has a `product_id` of 2)
  - WebSocket URL: `wss://gateway.prod.vertexprotocol.com/v1/ws`
- Implement proper error handling and reconnection mechanisms to ensure a reliable stream.

### Orderbook Builder

- Populate the internal orderbook with live data from the WebSocket client.
- Handle partial updates, as you won't receive the full orderbook on every message.
- Ensure the orderbook is valid:
  - Bids < Asks
  - Quantities > 0
  - Bids > 0 & Asks < ∞

### Entry Point

- Provide a way to start the WebSocket, use the Orderbook Builder to assemble orderbooks, and display the live orderbook to the user.
- Add detailed instructions for the entry point in the README file.
- Ensure accuracy of your bids & asks by inspection in the Vertex UI.

### Additional Considerations

- **Performance:** We are a trading firm and focus on writing high performance code. Keep this in mind in your implementation.
- **Error Handling:** Implement robust error handling for various scenarios, such as invalid requests or failed executions.
- **Logging:** Include logging to capture relevant events and debug information.
- **Assumptions:** Feel free to make reasonable assumptions where the case study details are unclear. Part of the task is to handle such ambiguities effectively.

### Documentation for Vertex

You can find the extensive documentation of Vertex [here](https://docs.vertexprotocol.com/developer-resources/api).

## Contributing

Contributions to improve and enhance the project are welcome. Please fork the repository, make changes, and submit a pull request for review.

## License

This project is licensed under the [MIT License](LICENSE), allowing for both personal and commercial use with proper attribution.

## Contact

For any inquiries regarding the project, feel free to send questions to tech@lhava.io.
