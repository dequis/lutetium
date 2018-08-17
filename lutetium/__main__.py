import click
import asyncio
import aioamqp
import logging
import functools

from .meter import Meter
from .pvsim import PVSim
from .sources import RandomMeterSource

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def run_forever(*coros):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*coros))
    loop.run_forever()
    return loop

@click.group()
@click.pass_context
def cli(ctx):
    setup_logging()
    ctx.obj['meter_source'] = RandomMeterSource()

def command(f):

    @cli.command(name=f.__name__)
    @click.pass_context
    @functools.wraps(f)
    def wrapper(ctx):
        run_forever(*f(ctx))

    wrapper.orig = f

    return wrapper

@command
def meter(ctx):
    return [Meter(**ctx.obj).run()]

@command
def pvsim(ctx):
    return [PVSim(**ctx.obj).run()]

@command
def all(ctx):
    return meter.orig(ctx) + pvsim.orig(ctx)

if __name__ == '__main__':
    cli(obj={})

