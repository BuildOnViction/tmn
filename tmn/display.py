import click


def link(msg, url):
    """
    Display a line formated for browser links

    :param msg: message
    :param url: website url
    """
    click.echo("{} {}".format(
        click.style(msg, fg='green'),
        click.style(url, fg='yellow', underline=True)
    ))


def error(msg):
    """
    Display a line formated for errors

    :param msg: error message
    """
    click.secho(f'! error: {msg}\n', fg='red')


def warning(msg):
    """
    Display a line formated for warnings

    :param msg: warning message
    """
    click.secho(f'! warn: {msg}\n', fg='yellow')
