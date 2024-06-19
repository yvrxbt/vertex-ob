Here's the updated and improved version of your README.md file:

# Project Name: Websocket with Internal Orderbook

## Introduction

This project aims to develop a simple Python application that streams a live orderbook for BTC (Bitcoin) from the on-chain perpetual exchange, Vertex. You'll need to recreate the orderbook using a stream of updates received from the exchange's public WebSocket. No API keys are required, but you will need a VPN to connect to the WebSocket if subscribing inside the United States. You may use any resources available, including AI tools like ChatGPT.

To pass this case study, you need to demonstrate the following:

## Must Complete

1. **WebSocket Client:** Implement a WebSocket client to communicate with Vertex and stream orderbook updates via the Book Depth stream.

2. **Orderbook Builder:** Develop a class to process and build the orderbook from the streamed updates.

3. **Entrypoint / Orderbook Display:** Provide an entry point to the application that displays the assembled orderbook *live* to the user. We will run your code from this entry point and compare the output to a live Vertex orderbook to judge accuracy.

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
- Aim for ~1-second latency between the live Vertex orderbook and your internal orderbook. No need for a verification system; just ensure accuracy by inspection.

### Additional Considerations

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

For any inquiries or suggestions regarding the project, feel free to contact Lhava at sam@lhava.io or ata@lhava.io.
