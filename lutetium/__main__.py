import os
import json
import click
import asyncio
import aioamqp
import logging
import functools

from .meter import Meter
from .pvsim import PVSim
from .writer import Writer
from .sources import SOURCE_REGISTRY

TASKS = {
    'meter': [Meter],
    'pvsim': [PVSim],
    'writer': [Writer],
}

TASKS['all'] = [x[0] for x in TASKS.values()]

source_choice = click.Choice(SOURCE_REGISTRY.keys())

@click.command()
@click.option('-v', '--verbose', count=True)
@click.option('-f', '--filename', default='out.jsonl')
@click.option('--meter-source',
    type=source_choice,
    default='random'
)
@click.option('--pvsim-source',
    type=source_choice,
    default='noisy_absurd_polynomial'
)
@click.argument('tasks',
    nargs=-1,
    required=True,
    type=click.Choice(TASKS.keys())
)
def main(verbose, filename, meter_source, pvsim_source, tasks):
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]

    logging.basicConfig(level=levels[min(2, verbose)])

    obj = {}
    obj['meter_source'] = SOURCE_REGISTRY[meter_source]()
    obj['pvsim_source'] = SOURCE_REGISTRY[pvsim_source]()
    obj['filename'] = filename

    if os.getenv('LUTETIUM_AMQP_CONFIG'):
        obj['amqp_config'] = json.loads(os.getenv('LUTETIUM_AMQP_CONFIG'))

    coros = []

    for name in tasks:
        for cls in TASKS[name]:
            instance = cls(**obj)
            coros.append(instance.run())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*coros))

if __name__ == '__main__':
    main()
