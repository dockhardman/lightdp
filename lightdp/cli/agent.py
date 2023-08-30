from typing import Text

import click
from rich import print

from lightdp.agent import AgentPool
from lightdp.broker import RedisBroker


@click.group()
def agent():
    pass


@click.command()
@click.option(
    "--name",
    "-n",
    required=False,
    default="AgentPool",
    envvar="AGENT_NAME",
    help="Agent name",
)
@click.option(
    "--broker_url",
    "-b",
    required=False,
    default="redis://localhost:6379/0",
    envvar="BROKER_URL",
    help="Broker URL",
)
@click.option(
    "--channel_name",
    "--channel",
    "-c",
    required=False,
    default="default",
    envvar="CHANNEL_NAME",
    help="Channel name",
)
def run(name: Text, broker_url: Text, channel_name: Text):
    print(f"Agent name: '{name}'")
    agent = AgentPool(name=name)

    print(f"Broker URL: '{broker_url}'")
    broker = RedisBroker(url=broker_url)
    broker.touch(channel_name=channel_name)
    print(f"{broker.__class__.__name__} connected!")

    agent.run(broker=broker, channel_name=channel_name)


agent.add_command(run)
