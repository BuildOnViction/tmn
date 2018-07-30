import sys
import click
from tmn import display
from tmn.config import ConfigManager


conf = None


@click.group()
@click.option('--config', help='Optional path to the config file')
@click.version_option()
def main(config):
    """
    Tomo masternode (tmn) is a cli tool to help you run a Tomochain masternode.

    :param config: path to the configuration file
    :type config: string
    """
    if config:
        conf = ConfigManager(config)
    else:
        conf = ConfigManager()
    if not conf.init():
        display.error('could not access configuration file')
        sys.exit()


@click.command()
@click.option('--open', is_flag=True, help='Open directly in your browser')
def docs(open):
    """
    Link to the documentation.

    :param open: open the link in your navigator
    :type open: bool
    """
    link = 'https://docs.tomochain.com/'
    if not open:
        display.link(
            'Documentation on running a masternode:',
            link
        )
    else:
        display.link('Opening documentation:', link)
        click.launch(link)

# @click.command(help='Initialize your masternode')
# def init():
#     """
#     Init
#     """
#     pass


main.add_command(docs)
# main.add_command(init)
