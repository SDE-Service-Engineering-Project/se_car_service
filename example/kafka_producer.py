"""
 Copyright 2015-2018 IBM

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

 Licensed Materials - Property of IBM
 © Copyright IBM Corp. 2015-2018
"""
import asyncio
import datetime
import json

from bson import ObjectId
from confluent_kafka import Producer


class ProducerTask(object):

    def __init__(self, conf, topic_name):
        self.topic_name = topic_name
        self.producer = Producer(conf)
        self.counter = 0
        self.running = True

    def stop(self):
        self.running = False

    def on_delivery(self, err, msg):
        if err:
            print('Delivery report: Failed sending message {0}'.format(msg.value()))
            print(err)
            # We could retry sending the message
        else:
            print('Message produced, offset: {0}'.format(msg.offset()))

    async def run(self):
        print('The producer has started')
        while self.running:

            message = {
                "id": str(ObjectId()),
                "carId": "64254a66a468c0902635a358",
                "startDate": 1672527600,
                "endDate": 1673305200,
                "action": "create"
            }
            key = 'key'
            sleep = 10  # Short sleep for flow control
            try:
                self.producer.produce(self.topic_name, json.dumps(message), key, -1, self.on_delivery)
                self.producer.poll(0)
                self.counter += 1
            except Exception as err:
                print('Failed sending message {0}'.format(message))
                print(err)
                sleep = 5  # Longer sleep before retrying
            await asyncio.sleep(sleep)
        self.producer.flush()
