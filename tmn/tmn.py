import logging
import sys

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
    configuration = Configuration(name=name, net=net, pkey=pkey, start=True)
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
    # container
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


@click.command(help='Stop your Tomochain masternode')
def stop() -> None:
    "Stop the masternode containers"
    configuration = Configuration()
    display.title_stop_masternode(configuration.name)
    for _, service in configuration.services.items():
        display.step_stop_container(service.name)
        if service.stop():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()


@click.command(help='Show the status of your Tomochain masternode')
def status():
    "Show the status of the masternode containers"
    configuration = Configuration()
    display.title_status_masternode(configuration.name)
    for _, service in configuration.services.items():
        status = service.status()
        if status and status == 'absent':
            display.status(
                name=service.name
            )
        if status and status in ['running']:
            display.status(
                name=service.name,
                status=status,
                id=service.container.short_id,
                status_color='green'
            )
        elif status:
            display.status(
                name=service.name,
                status=status,
                id=service.container.short_id,
            )
        else:
            display.status(
                name=service.name,
                status='error'
            )
    display.newline()


@click.command(help='Remove your Tomochain masternode')
@click.option('--confirm', is_flag=True)
def remove(confirm: bool) -> None:
    "Remove the masternode (containers, networks volumes)"
    configuration = Configuration()
    if not confirm:
        display.warning_remove_masternode(configuration.name)
        sys.exit()
    display.title_remove_masternode(configuration.name)
    display.subtitle_remove_containers()
    # containers
    # stop
    for _, service in configuration.services.items():
        display.step_stop_container(service.name)
        if service.stop():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()
    # remove
    for _, service in configuration.services.items():
        display.step_remove_container(service.name)
        if service.remove():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()
    # networks
    display.subtitle_remove_networks()
    for _, network in configuration.networks.items():
        display.step_remove_network(network.name)
        if network.remove():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()
    # volumes
    display.subtitle_remove_volumes()
    for _, volume in configuration.volumes.items():
        display.step_remove_volume(volume.name)
        if volume.remove():
            display.step_close('✔')
        else:
            display.step_close('✗', 'red')
    display.newline()
    configuration.remove()


main.add_command(docs)
main.add_command(start)
main.add_command(stop)
main.add_command(status)
main.add_command(remove)
