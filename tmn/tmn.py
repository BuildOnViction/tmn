import click
from tmn import display


@click.group()
def main():
    """
    Tomo masternode (tmn) is a cli tool to help you run a Tomochain masternode.
    """
    pass


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
            'You can find documentation on running a masternode here:',
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
