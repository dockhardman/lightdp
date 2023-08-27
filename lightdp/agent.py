from abc import ABC
from typing import Text, Union

from lightdp.job import Job, JobType
from lightdp.runner import DockerRunner, Runner


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
