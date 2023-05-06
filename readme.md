# Currency Converter
The currency converter retrieves the current exchange rates from the European Central Bank (ECB) daily, caches them, and offers two operations to the booking_service via gRPC.

## Tools and Technologies

* Language: Python 3.11
* XML parsing library: lxml
* gRPC library: grpcio
* Test framework: Pytest

## Data Model

None, the currencies are not persisted in any database. The rates are only kept in memory.

## Description of Interactions between Microservices
The currency converter only calls one downstream system, which is not part of the implementation, namely the ECB website hosting the currency exchange rates.

The currency exchange rate cache is cleared daily at 5 PM UTC / 7 PM CET. The ECB renews the file daily at around 4 PM CET, however, they do not always renew it exactly at the same time, therefore these few hours buffer.