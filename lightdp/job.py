import json
from abc import ABC
from enum import Enum
from typing import Optional, Text, TypedDict, Union


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


class JobDict(TypedDict):
    job_type: Text


class DockerRunJobDict(JobDict):
    image_name: Text
    port: Optional[Text]
    cpu: Text
    memory: Text


class Job(ABC):
    def __init__(self, job_type: "JobType", **kwargs):
        self.job_type = JobType.from_string(job_type)

    def dict(self):
        return JobDict(job_type=self.job_type.value)

    def json(self, **kwargs):
        return json.dumps(self.dict(), **kwargs)

    @classmethod
    def from_raw(cls, raw: Union[Text, bytes]) -> "Job":
        job_dict = json.loads(raw)
        job_type = JobType.from_string(job_dict["job_type"])
        if job_type == JobType.DOCKER_RUN:
            return DockerRunJob(**job_dict)
        else:
            raise ValueError(f"Not supported job type: {job_type}")


class DockerRunJob(Job):
    def __init__(
        self,
        job_type: "JobType",
        image_name: Text,
        port: Optional[Text] = None,
        cpu: Text = "500m",
        memory: Text = "512Mi",
        **kwargs,
    ):
        super().__init__(job_type=JobType.DOCKER_RUN, **kwargs)

        self.image_name = image_name
        self.port = port
        self.cpu = cpu
        self.memory = memory

    def dict(self):
        return DockerRunJobDict(
            job_type=self.job_type.value,
            image_name=self.image_name,
            port=self.port,
            cpu=self.cpu,
            memory=self.memory,
        )
