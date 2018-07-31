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
              help='Optional path to the config file')
@click.version_option()
def main(config):
    """
    Cli entrypoint.

    :param config: path to the configuration file
    :type config: string
    """
    if config:
        conf = ConfigManager(config)
    else:
        conf = ConfigManager()
    if not conf.valid:
        display.error('could not access or create configuration file')
        sys.exit()
    if not masternode.up:
        display.error('could not access the docker deamon')
        sys.exit()


@click.command(help='Display Tomochain documentation link')
@click.option('--open', is_flag=True, help='Open directly in your browser')
def docs(open):
    """
    Link to the documentation

    :param open: open the link in your navigator
    :type open: bool
    """
    link = 'https://docs.tomochain.com/'
    if not open:
        display.link('Documentation on running a masternode:', link)
    else:
        display.link('Opening documentation:', link)
        click.launch(link)


@click.command(help='Start your Tomochain Masternode on Docker')
def start():
    """
    Start the containers needed to run a masternode
    """
    masternode.start()

main.add_command(docs)
main.add_command(start)
