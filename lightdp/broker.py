from abc import ABC
from typing import Generator, Text

import redis

from lightdp.job import Job


class Broker(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def publish(self, channel_name: Text, message: Text, *args, **kwargs):
        raise NotImplementedError

    def subscribe(
        self, channel_name: Text, *args, **kwargs
    ) -> Generator[Job, None, None]:
        raise NotImplementedError


class RedisBroker(Broker):
    def __init__(self, url: Text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = redis.from_url(url)

    def publish(self, channel_name: Text, message: Text, *args, **kwargs):
        self.client.publish(channel_name, message)

    def subscribe(
        self, channel_name: Text, *args, **kwargs
    ) -> Generator["Job", None, None]:
        pubsub = self.client.pubsub()
        pubsub.subscribe(channel_name)
        for message in pubsub.listen():
            if message["type"] == "message":
                raw_data: bytes = message["data"]
                job = Job.from_raw(raw_data)
                yield job
