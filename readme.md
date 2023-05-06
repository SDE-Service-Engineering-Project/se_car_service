# Car Service
The car service manages cars which are persisted in a MongoDB, retrieves bookings from a Kafka topic and stores a subset of the booking-information in MongoDB.
## Tools and technologies
### Libraries
* Language:				Python 3.11
* Web Framework:			StarLite 1.5
* Mongo Client:				Pymongo
* Kafka Consumer:			confluent-kafka
* Test framework: 			Pytest
### Other technology
* Persistent Storage:			MongoDB (Atlas Cloud DB)
* IBM Event Streams (Kafka):		IBM Event Streams (free version)
## Data model
The service persists two types of data elements: cars and a slimmed-down version of bookings in MongoDB.
Cars and bookings are stored within the same database in individual collections.

## Description of interactions between microservices
As shown in the architecture overview, the service is accessed by the API gateway (list cars, list available cars), as well as by the booking service (get car) via REST.
Additionally, the service consumes booking messages from Kafka produced by the booking service and persists them in MongoDB.
