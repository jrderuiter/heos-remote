import logging
from typing import Iterable

import click

from .events import EvdevEventListener
from .player import get_player, get_group
from .remote import PlayerRemote

logging.basicConfig(
    format="[%(asctime)-15s] %(name)s (%(levelname)s) - %(message)s",
    level=logging.INFO
)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--device", required=True, multiple=True)
@click.option("--name", required=True)
@click.option("--rediscover", is_flag=True)
def player(device: Iterable[str], name: str, rediscover: bool):
    player = get_player(name, rediscover=rediscover)
    remote = PlayerRemote(player)

    listeners = [EvdevEventListener(dev) for dev in device]
    remote.start(listeners)


@cli.command()
@click.option("--device", required=True, multiple=True)
@click.option("--name", required=True)
@click.option("--rediscover", is_flag=True)
def group(device: Iterable[str], name: str, rediscover: bool):
    group = get_group(name, rediscover=rediscover)
    remote = PlayerRemote(group)

    listeners = [EvdevEventListener(dev) for dev in device]
    remote.start(listeners)


if __name__ == "__main__":
    cli()
