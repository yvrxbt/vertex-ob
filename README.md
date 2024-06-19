# Project Name: RESTful API with Internal Orderbook

## Introduction

This project aims to develop simple application in Python that serves a single function: stream a single live orderbook for BTC (Bitcoin) from the onchain perp exchange Vertex. You will need to recreate the orderbook given a stream of updates received from the exchange's public websocket. No API keys are required, but you will need a VPN to connect to the websocket if subscribing inside the United States. Any resource available to you is allowed (including AI tools like Chat-GPT).

To pass this case study, you need to demonstrate the following...

## Must Complete

1. **Websocket Client:** A websocket client to specifically communicate with Vertex to stream order book updates. 

2. **Orderbook Builder:** The websocket will stream orderbook updates from different depths in the book, but you need an object to process the streamed events. 

3. **Entrypoint / Orderbook Display:** Provide us with an entrypoint to the application which will display the orderbooks *live* from the orderbook builder class to the user. We will run your code from this entrypoint and compare the output to a live vertex orderbook to judge the accuracy of the case study. Attempt to target ~1sec latency (which is quite doable even with Python)

## Implementation Details

### Websocket Client

- You can find documentation from Vertex [here](https://docs.vertexprotocol.com/developer-resources/api/subscriptions/events#book-depth). You cannot use the Python SDK for this project, implement everything yourself!
- You have the option of building a sync or async client. If you choose a synchronous design, use threading and locks to handle race conditions. If you use async websockets, ensure that your entire app is async in nature. It is important to remain consistent in how you build!
- Focus on the orderbook for BTC on the Aribtrum One blockchain. There are many tickers and chains you can choose from, but keep it simple for this case study:
  - `ticker: BTC`
  - `wss: wss://gateway.prod.vertexprotocol.com/v1/ws`
- Proper error handling and reconnection handlers are important as a failure in the websocket to consistently stream will be seen as an incomplete case study.

### Orderbook Builder

- The internal orderbook is populated with live data obtained from Vertex Protocol using the websocket client.
- Remember that you will receive order book updates from the websocket, so do not assume that you will get the full orderbook on every message.
- You will want to be able to display the final orderbook somehow when we run your code from the entry point, so keep this in mind when you are building.
- At a minimum, you shoud ensure that orderbooks are valid
  - Bids < Asks
  - Quantities > 0
  - Bids > 0 & Asks < inf

### Entry Point

- Provide us with the ability to start the websocket, use the Orderbook builder to assemble orderbooks, and display the live internal orderbook to the user.
- Add instructions for the entry point in a README file.
- Attempt to target ~1sec latency between the live Vertex orderbook and the internally assembled orderbook you display. No need to build a verification system, just eyeball that your internal orderbook feed is accurate.

### Additional Considerations

- Error handling: Implement robust error handling mechanisms to handle various scenarios, such as invalid requests or failed executions.
- Logging: Implement logging to capture relevant events and debug information for monitoring and troubleshooting purposes.
- Assumptions: Feel free to make assumptions on the unclear parts of the case study, one of our job is making assumptions with limited knowledge we get from exchanges.

### Documentation for Vertex

You can find the full, extensive documentation of Vertex in [Vertex Documentation](https://docs.vertexprotocol.com/developer-resources/api):

## Contributing

Contributions to improve and enhance the project are welcome. Please fork the repository, make changes, and submit a pull request for review.

## License

This project is licensed under the [MIT License](LICENSE), allowing for both personal and commercial use with proper attribution.

## Contact

For any inquiries or suggestions regarding the project, feel free to contact Lhava at sam@lhava.io or ata@lhava.io
