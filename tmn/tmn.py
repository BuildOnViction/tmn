import sys
import click
from tmn import display
from tmn.config import ConfigManager
from tmn import masternode


conf = None


@click.group(help='Tomo MasterNode (tmn) is a cli tool to help you run a '
             + 'Tomochain masternode')
@click.option('--config',
              metavar='PATH',
              help='Path to the config file')
@click.option('--dockerurl',
              metavar='URL',
              help='Url to the docker server')
@click.version_option()
def main(config, dockerurl):
    """
    Cli entrypoint.

    :param config: path to the configuration file
    :type config: str
    """
    if config:
        conf = ConfigManager(config)
    else:
        conf = ConfigManager()
    if not conf.valid:
        display.error_config()
        sys.exit()
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


@click.command(help='Start your Tomochain masternode')
def start():
    """
    Start the containers needed to run a masternode
    """
    display.title_start_masternode()
    masternode.start()


@click.command(help='Stop your Tomochain masternode')
def stop():
    """
    Stop the containers needed to run a masternode
    """
    display.title_stop_masternode()
    # masternode.stop()


main.add_command(docs)
main.add_command(start)
main.add_command(stop)
