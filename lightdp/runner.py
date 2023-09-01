from abc import ABC
from typing import TYPE_CHECKING, Text

import docker

from lightdp.job import DockerRunJob

if TYPE_CHECKING:
    from docker.models.containers import Container


class Runner(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        raise NotImplementedError

    def run_job(self, job: "DockerRunJob", *args, **kwargs):
        raise NotImplementedError

    def logs(self, *args, **kwargs):
        raise NotImplementedError


class DockerRunner(Runner):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.client = docker.from_env()

    def run(self, image_name: Text, *args, **kwargs):
        container_id = self.run_docker_image(image_name)
        self.logs(container_id)

    def run_job(self, job: "DockerRunJob", *args, **kwargs):
        if not isinstance(job, DockerRunJob):
            raise ValueError(f"Invalid job type: {type(job)}")

        self.run(job.image_name, *args, **kwargs)

    def logs(self, container_id: Text, *args, **kwargs):
        container: "Container" = self.client.containers.get(container_id)
        for line_bytes in container.logs(stream=True):
            line_bytes: bytes
            print(line_bytes.decode("utf-8").strip())

    def run_docker_image(self, image_name: Text):
        print(f"Starting container from image: {image_name}")
        container = self.client.containers.run(
            image_name,
            runtime="runc",
            # command=None,
            detach=True,
            auto_remove=True,
            environment=[],
        )
        print(f"Started container: {container.id}")
        return container.id
