import sys
import click
from tmn import __version__
from tmn import display
from tmn import masternode


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
    masternode.connect(url=dockerurl)
    if masternode.connected is False:
        display.error_docker()
        sys.exit()


@click.command(help='Display Tomochain documentation link')
@click.option('--open', is_flag=True, help='Open directly in your browser')
def docs(open):
    """
    Link to the documentation

    :param open: open the link in your navigator
    :type open: bool
    """
    url = 'https://docs.tomochain.com/'
    if not open:
        display.link_docs(url)
    else:
        display.link_docs_open(url)
        click.launch(url)


@click.command(help='List local Tomochain masternodes')
def list():
    """
    List the currently existing Tomochain masternodes
    """
    display.title_list_masternodes()
    masternode.list_masternodes()


@click.command(help='Start your Tomochain masternode')
@click.argument('name')
def start(name):
    """
    Start the containers needed to run a masternode
    """
    display.title_start_masternode(name)
    masternode.start(name)


@click.command(help='Stop your Tomochain masternode')
@click.argument('name')
def stop(name):
    """
    Stop the containers needed to run a masternode
    """
    display.title_stop_masternode(name)
    masternode.stop(name)


@click.command(help='Status of your Tomochain masternode')
@click.argument('name')
def status(name):
    """
    Display the status of the masternode containers
    """
    display.title_status_masternode(name)
    masternode.status(name)


main.add_command(docs)
main.add_command(list)
main.add_command(start)
main.add_command(stop)
main.add_command(status)
