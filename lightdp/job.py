from abc import ABC
from enum import Enum
from typing import Optional, Text, Union


class JobType(str, Enum):
    DOCKER_RUN = "docker_run"

    @classmethod
    def from_string(cls, s: Union[Text, "JobType"]):
        if isinstance(s, JobType):
            return s
        s_casefold = s.casefold()
        for job_type in cls:
            if job_type.value.casefold() == s_casefold:
                return job_type
        raise ValueError(
            f"Invalid job type: {s}, "
            + f"valid job types are: {', '.join(cls.__members__.keys())}"
        )


class Job(ABC):
    def __init__(
        self, job_type: "JobType", cpu: Text = "500m", memory: Text = "512Mi", **kwargs
    ):
        self.job_type = JobType.from_string(job_type)
        self.cpu = cpu
        self.memory = memory


class DockerRunJob(Job):
    def __init__(
        self,
        image_name: Text,
        port: Optional[Text] = None,
        cpu: Text = "500m",
        memory: Text = "512Mi",
        **kwargs,
    ):
        super().__init__(JobType.DOCKER_RUN, cpu=cpu, memory=memory, **kwargs)

        self.image_name = image_name
        self.port = port
