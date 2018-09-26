import logging

import click

from tmn import display
from tmn import __version__
from tmn.configuration import Configuration

logger = logging.getLogger('tmn')


@click.group(help=('Tomo MasterNode (tmn) is a cli tool to help you run a Tomo'
                   'chain masternode'))
@click.option('--debug', is_flag=True, help='Enable debug mode')
@click.version_option(version=__version__)
def main(debug: bool) -> None:
    "Cli entrypoint"
    if debug:
        logger.setLevel('DEBUG')
        logger.debug('Debugging enabled')


@click.command(help='Display Tomochain documentation link')
def docs() -> None:
    "Link to the documentation"
    display.link_docs()


@click.command(help='Start your Tomochain masternode')
@click.option('--name', metavar='NAME', help='Your masternode\'s name')
@click.option('--net', type=click.Choice(['testnet', 'devnet']),
              help='The environment your masternode will connect to')
@click.option('--pkey', metavar='KEY', help=('Private key of the account your '
                                             'masternode will collect rewards '
                                             'on'))
def start(name: str, net: str, pkey: str) -> None:
    "Start the containers needed to run a masternode"
    configuration = Configuration(name=name, net=net, pkey=pkey)
    display.title_start_masternode(configuration.name)
    # volumes
    display.subtitle_create_volumes()
    for _, value in configuration.volumes.items():
        display.step_create_volume(value.name)
        if value.create():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()
    # networks
    display.subtitle_create_networks()
    for _, value in configuration.networks.items():
        display.step_create_network(value.name)
        if value.create():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()
    # containers
    # create
    display.subtitle_create_containers()
    for _, value in configuration.services.items():
        display.step_create_container(value.name)
        if value.create():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()
    # start
    for _, value in configuration.services.items():
        display.step_start_container(value.name)
        if value.start():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()


main.add_command(docs)
main.add_command(start)
