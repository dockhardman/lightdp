from abc import ABC
from typing import TYPE_CHECKING, Text, Union

from lightdp.job import Job, JobType
from lightdp.runner import DockerRunner, Runner

if TYPE_CHECKING:
    from lightdp.broker import Broker


class AgentPoolBase(ABC):
    def __init__(self, name: Text = "default", *args, **kwargs):
        self.name = name

    def run(self, broker: "Broker", channel_name: Text, *args, **kwargs):
        for job in broker.subscribe(channel_name=channel_name, *args, **kwargs):
            self.consume(job=job, *args, **kwargs)

    def dispatch(self, job_type: Union[Text, "JobType"], *args, **kwargs) -> "Runner":
        job_type = JobType.from_string(job_type)
        if job_type == JobType.DOCKER_RUN:
            return DockerRunner(*args, **kwargs)
        else:
            raise ValueError(f"Not supported job type: {job_type}")

    def consume(self, job: "Job", *args, **kwargs):
        runner = self.dispatch(job.job_type, *args, **kwargs)
        runner.run_job(job=job, *args, **kwargs)


class AgentPool(AgentPoolBase):
    def __init__(self, name: Text = "default", *args, **kwargs):
        super().__init__(name=name, *args, **kwargs)
