from abc import ABC
from enum import Enum
from typing import Text, Union

from lightdp.runner import DockerRunner, Runner


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
    def __init__(self, job_type: "JobType", **kwargs):
        self.job_type = JobType.from_string(job_type)


class AgentPoolBase(ABC):
    def __init__(self, *args, **kwargs):
        pass

    def dispatch(self, job_type: Union[Text, "JobType"], *args, **kwargs) -> "Runner":
        job_type = JobType.from_string(job_type)
        if job_type == JobType.DOCKER_RUN:
            return DockerRunner(*args, **kwargs)
        else:
            raise ValueError(f"Not supported job type: {job_type}")

    def consume(self, job: "Job", *args, **kwargs):
        runner = self.dispatch(job.job_type, *args, **kwargs)
        runner.run(*args, **kwargs)


class AgentPool(AgentPoolBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
