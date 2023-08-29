from typing import Text

import click

from lightdp.agent import AgentPool
from lightdp.broker import RedisBroker


@click.group()
def agent():
    pass


@click.command()
@click.option(
    "--agent_name", "-a", required=False, default="AgentPool", help="Agent name"
)
@click.option(
    "--broker_url",
    "-b",
    required=False,
    default="redis://localhost:30466/0",
    help="Broker URL",
)
@click.option(
    "--channel_name", "-c", required=False, default="default", help="Channel name"
)
def run(agent_name: Text, broker_url: Text, channel_name: Text):
    agent = AgentPool(name=agent_name)
    broker = RedisBroker(url=broker_url)
    agent.run(broker=broker, channel_name=channel_name)


agent.add_command(run)
