from abc import ABC
from typing import Text

import redis


class Broker(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def publish(self, channel_name: Text, message: Text, *args, **kwargs):
        raise NotImplementedError

    def subscribe(self, channel_name: Text, *args, **kwargs):
        raise NotImplementedError


class RedisBroker(Broker):
    def __init__(self, url: Text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = redis.from_url(url)

    def publish(self, channel_name: Text, message: Text, *args, **kwargs):
        self.client.publish(channel_name, message)

    def subscribe(self, channel_name: Text, *args, **kwargs):
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel_name)
        for message in pubsub.listen():
            if message["type"] == "message":
                print(message["data"].decode("utf-8"))
