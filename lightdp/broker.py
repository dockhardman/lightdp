from abc import ABC
from typing import Generator, Text

import redis

from lightdp.job import Job


class Broker(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def ping(self, *args, **kwargs) -> bool:
        raise NotImplementedError

    def touch(self, channel_name: Text, *args, **kwargs):
        raise NotImplementedError

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

    def ping(self, *args, **kwargs) -> bool:
        return self.client.ping(*args, **kwargs)

    def touch(self, channel_name: Text, *args, **kwargs):
        return self.ping(*args, **kwargs)

    def publish(self, channel_name: Text, job: "Job", *args, **kwargs):
        self.client.lpush(channel_name, job.json())

    def subscribe(
        self, channel_name: Text, *args, **kwargs
    ) -> Generator["Job", None, None]:
        while True:
            _, raw_data = self.client.brpop(channel_name)
            job = Job.from_raw(raw_data)
            yield job
