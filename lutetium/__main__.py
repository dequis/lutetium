import click
import asyncio
import aioamqp
import logging

from .meter import Meter
from .pvsim import PVSim

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def run_forever(*coros):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*coros))
    loop.run_forever()
    return loop

@click.group()
def cli():
    setup_logging()

@cli.command()
def meter():
    run_forever(Meter().run())

@cli.command()
def pvsim():
    run_forever(PVSim().run())

@cli.command()
def all():
    run_forever(
        Meter().run(),
        PVSim().run(),
    )

if __name__ == '__main__':
    cli()

