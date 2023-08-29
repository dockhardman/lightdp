import click

from lightdp.cli.agent import agent as agent_cli
from lightdp.version import VERSION


@click.group()
def app():
    pass


@click.command()
@click.option("-vv", "-v", "verbose", is_flag=True, default=False, help="Verbose mode")
@click.option("-s", "--short", "short", is_flag=True, default=False, help="Short mode")
def version(verbose: bool, short: bool):
    if short:
        click.echo(VERSION)
    else:
        click.echo(f"lightdp version {VERSION}")
        if verbose:
            click.echo("Verbose mode enabled")


app.add_command(version)
app.add_command(agent_cli)
