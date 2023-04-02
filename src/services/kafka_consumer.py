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
import logging

from confluent_kafka import Consumer

log = logging.getLogger()


class ConsumerTask(object):
    def __init__(self, servers, username, api_token, topic_name):
        self.driver_options = {
            'bootstrap.servers': servers,
            'security.protocol': 'SASL_SSL',
            'sasl.mechanisms': 'PLAIN',
            'sasl.username': username,
            'sasl.password': api_token,
            'api.version.request': True,
            'broker.version.fallback': '0.10.2.1',
            'log.connection.close': False,
        }
        self.client_options = {'client.id': 'kafka-se-car-service-consumer',
                               'group.id': 'service-engineering'}
        self.consumer = Consumer({**self.driver_options, **self.client_options})
        self.topic_name = topic_name
        self.running = True
        self.event_handlers = []

    def add_event_handler(self, handler):
        self.event_handlers.append(handler)

    def remove_event_handler(self, handler):
        self.event_handlers.remove(handler)

    def fire_event(self, event):
        for handler in self.event_handlers:
            handler(event)

    def stop(self):
        self.running = False

    async def run(self):
        print('The consumer has started')
        self.consumer.subscribe([self.topic_name])
        while self.running:
            msg = self.consumer.poll(1)
            if msg is not None and msg.error() is None:
                log.info('Message consumed: topic={0}, partition={1}, offset={2}, key={3}, value={4}'.format(
                    msg.topic(),
                    msg.partition(),
                    msg.offset(),
                    msg.key().decode('utf-8'),
                    msg.value().decode('utf-8')))
                self.fire_event(msg.value().decode('utf-8'))
            else:
                await asyncio.sleep(1)
        self.consumer.unsubscribe()
        self.consumer.close()


async def run_consumer(consumer):
    tasks = [asyncio.ensure_future(consumer.run())]
    done, pending = await asyncio.wait(tasks)
    for future in done | pending:
        future.result()