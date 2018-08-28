import sys
import click
from tmn import __version__
from tmn import display
from tmn import masternode
from tmn import configuration

conf = None


@click.group(help='Tomo MasterNode (tmn) is a cli tool to help you run a '
             + 'Tomochain masternode')
@click.option('--dockerurl',
              metavar='URL',
              help='Url to the docker server')
@click.version_option(version=__version__)
def main(dockerurl):
    """
    Cli entrypoint.

    :param config: path to the configuration file
    :type config: str
    """
    if not masternode.connect(url=dockerurl):
        display.error_docker()
        sys.exit()


@click.command(help='Display Tomochain documentation link')
def docs():
    """
    Link to the documentation

    :param open: open the link in your navigator
    :type open: bool
    """
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
def start(name, net, pkey):
    """
    Start the containers needed to run a masternode
    """
    configuration.init(name, net, pkey)
    display.title_start_masternode(configuration.name)
    masternode.start(configuration.name)


@click.command(help='Stop your Tomochain masternode')
def stop():
    """
    Stop the containers needed to run a masternode
    """
    configuration.init()
    display.title_stop_masternode(configuration.name)
    masternode.stop(configuration.name)


@click.command(help='Show the status of your Tomochain masternode')
def status():
    """
    Show the status of the masternode containers
    """
    configuration.init()
    display.title_status_masternode(configuration.name)
    masternode.status(configuration.name)


@click.command(help='Show details about your Tomochain masternode')
def inspect():
    """
    Show details about the tomochain masternode
    """
    configuration.init()
    display.title_inspect_masternode(configuration.name)
    masternode.details(configuration.name)


@click.command(help='Remove your Tomochain masternode')
@click.option('--confirm', is_flag=True)
def remove(confirm):
    """
    Remove the masternode completly (containers, networks volumes)
    """
    configuration.init()
    if not confirm:
        display.warning_remove_masternode(configuration.name)
        sys.exit()
    display.title_remove_masternode(configuration.name)
    masternode.remove(configuration.name)


main.add_command(docs)
main.add_command(start)
main.add_command(stop)
main.add_command(status)
main.add_command(inspect)
main.add_command(remove)
