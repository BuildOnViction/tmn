import sys
import click

from tmn import __version__
from tmn import display
from tmn import configuration
from tmn import elements

conf = None
volume_chaindata = elements.Volume(
    name='chaindata'
)
network_default = elements.Network(
    name='tmn_default'
)
service_metrics = elements.Service(
    image='tomochain/telegraf:latest',
    name='metrics',
    network='tmn_default',
    volumes={
      '/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'ro'},
      '/sys': {'bind': '/rootfs/sys', 'mode': 'ro'},
      '/proc': {'bind': '/rootfs/proc', 'mode': 'ro'},
      '/etc': {'bind': '/rootfs/etc', 'mode': 'ro'}
    }
)
service_tomochain = elements.Service(
    image='tomochain/node:latest',
    name='tomochain',
    network='tmn_default',
    volumes={
        'chaindata': {'bind': '/tomochain/data', 'mode': 'rw'}
    },
    ports={
        '30303/udp': 30303, '30303/tcp': 30303
    }
)


@click.group(
    help=('Tomo MasterNode (tmn) is a cli tool to help you run a Tomochain'
          'masternode')
)
@click.option(
    '--docker_url',
    metavar='URL',
    help='Url to the docker server'
)
@click.version_option(version=__version__)
def main(docker_url: str) -> None:
    "Cli entrypoint"
    pass


@click.command(help='Display Tomochain documentation link')
def docs() -> None:
    "Link to the documentation"
    display.link_docs()


@click.command(help='Start your Tomochain masternode')
@click.option('--name',
              metavar='NAME',
              help='Your masternode\'s name')
@click.option('--net',
              type=click.Choice(['testnet', 'devnet']),
              help='The environment your masternode will connect to')
@click.option('--pkey',
              metavar='KEY',
              help=('Private key of the account your masternode will collect '
                    'rewards on'))
def start(name: str, net: str, pkey: str) -> None:
    "Start the containers needed to run a masternode"
    # configuration.init(name, net, pkey)
    display.title_start_masternode(configuration.name)
    # volumes
    display.subtitle_create_volumes()
    display.step_create_volume(volume_chaindata.name)
    if volume_chaindata.create():
        display.step_close('✔')
    else:
        display.step_close('✗')
    display.newline()
    # networks
    display.subtitle_create_networks()
    display.step_create_network(network_default.name)
    if network_default.create():
        display.step_close('✔')
    else:
        display.step_close('✗', 'red')
    display.newline()
    # containers
    # create
    display.subtitle_create_containers()
    display.step_create_container(service_metrics.name)
    if service_metrics.create():
        display.step_close('✔')
    else:
        display.step_close('✗', 'red')
    display.step_create_container(service_tomochain.name)
    if service_tomochain.create():
        display.step_close('✔')
    else:
        display.step_close('✗', 'red')
    display.newline()
    # start
    display.step_start_container(service_metrics.name)
    if service_metrics.start():
        display.step_close('✔')
    else:
        display.step_close('✗')
    display.step_start_container(service_tomochain.name)
    if service_tomochain.start():
        display.step_close('✔')
    else:
        display.step_close('✗', 'red')
    display.newline()


@click.command(help='Stop your Tomochain masternode')
def stop() -> None:
    "Stop the containers needed to run a masternode"
    configuration.init()
    display.title_stop_masternode(configuration.name)
    # masternode.stop(configuration.name)


@click.command(help='Show the status of your Tomochain masternode')
def status() -> None:
    "Show the status of the masternode containers"
    configuration.init()
    display.title_status_masternode(configuration.name)
    # masternode.status(configuration.name)


@click.command(help='Show details about your Tomochain masternode')
def inspect() -> None:
    "Show details about the tomochain masternode"
    configuration.init()
    display.title_inspect_masternode(configuration.name)
    # masternode.details(configuration.name)


@click.command(help='Remove your Tomochain masternode')
@click.option('--confirm', is_flag=True)
def remove(confirm: bool) -> None:
    "Remove the masternode completly (containers, networks volumes)"
    configuration.init()
    if not confirm:
        display.warning_remove_masternode(configuration.name)
        sys.exit()
    display.title_remove_masternode(configuration.name)
    # masternode.remove(configuration.name)


main.add_command(docs)
main.add_command(start)
main.add_command(stop)
main.add_command(status)
main.add_command(inspect)
main.add_command(remove)
