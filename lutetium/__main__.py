import click
import asyncio
import aioamqp
import logging
import functools

from . import sources
from .meter import Meter
from .pvsim import PVSim
from .writer import Writer

TASKS = {
    'meter': [Meter],
    'pvsim': [PVSim],
    'writer': [Writer],
}

TASKS['all'] = [x[0] for x in TASKS.values()]

def setup_logging(verbose):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]

    logging.basicConfig(level=levels[min(2, verbose)])

@click.command()
@click.option('-v', '--verbose', count=True)
@click.argument('tasks',
    nargs=-1,
    required=True,
    type=click.Choice(TASKS.keys())
)
def main(verbose, tasks):
    setup_logging(verbose)

    obj = {}
    obj['meter_source'] = sources.RandomMeterSource()
    obj['pvsim_source'] = sources.NoisyAbsurdPolynomialFitSource()
    obj['filename'] = 'out.jsonl'

    coros = []

    for name in tasks:
        for cls in TASKS[name]:
            instance = cls(**obj)
            coros.append(instance.run())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*coros))
    loop.run_forever()

if __name__ == '__main__':
    main()
