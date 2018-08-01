import pastel

pastel.add_style('highlight_g', 'green')
pastel.add_style('highlight_y', 'yellow')
pastel.add_style('link', 'yellow', options=['underscore'])
pastel.add_style('warning', 'yellow')
pastel.add_style('error', 'red')


def style(function):
    """
    Print and colorize strings with `pastel`

    :param function: the string returning function
    :type function: function
    """
    def wrapper(*args):
        print(pastel.colorize(function(*args)))
    return wrapper


def style_no_new_line(function):
    """
    Print and colorize strings with `pastel`. Don't add a new line at the end.

    :param function: the string returning function
    :type function: function
    """
    def wrapper(*args):
        print(pastel.colorize(function(*args)), end='', flush=True)
    return wrapper


@style
def link(msg, url):
    """
    Return a pastel formated string for browser links

    :param msg: message
    :param url: website url
    :type msg: string
    :type url: string
    """
    return '<highlight_g>{msg}</highlight_g> <link>{url}</link>'.format(
        msg=msg,
        url=url
    )


def link_docs(url):
    """
    Custom link message for documentation
    """
    link('Documentation on running a masternode:', url)


def link_docs_open(url):
    """
    Custom link message for documentation, 'open in browser' version
    """
    link('Opening documentation:', url)


@style
def title(msg):
    """
    Return a pastel formated title string

    :param msg: message
    :type msg: string
    """
    return '\n<highlight_g>{msg}</highlight_g>\n'.format(
        msg=msg
    )


def title_start_masternode():
    """
    Title when starting a masternode
    """
    title('Starting your masternode!')


@style_no_new_line
def step(msg):
    """
    Return a pastel formated step

    :param msg: message
    :type msg: string
    """
    return '    {msg}... '.format(
        msg=msg
    )


def step_start_masternode_volume(volume):
    """
    Custom step message for docker volumes creation
    """
    step('volume (<fg=yellow>{volume}</>)'.format(
        volume=volume
    ))


def step_start_masternode_network(network):
    """
    Custom step message for docker networks creatin
    """
    step('network (<fg=yellow>{network}</>)'.format(
        network=network
    ))


def step_start_masternode_container(container):
    """
    Custom step message for docker container starting
    """
    step('container (<fg=yellow>{container}</>)'.format(
        container=container
    ))


@style
def step_close(msg, color='green'):
    """
    Return a pastel formated end of step

    :param msg: message
    :type msg: string
    """
    return '<fg={color}>{msg}</>'.format(
        msg=msg,
        color=color
    )


def step_close_created():
    """
    Custom 'created' closing step message
    """
    step_close('created')


def step_close_exist():
    """
    Custom 'exist' closing step message
    """
    step_close('exist')


def step_close_exists():
    """
    Custom 'exists' closing step message
    """
    step_close('exists')


@style
def warning(msg):
    """
    Return a pastel formated string for warnings

    :param msg: warning message
    :type msg: string
    """
    return '<warning>! warning:</warning> {msg}\n'.format(
        msg=msg
    )


@style
def error(msg):
    """
    Return a pastel formated string for errors

    :param msg: error message
    :type msg: string
    """
    return '<error>! error:</error> {msg}\n'.format(
        msg=msg
    )


def error_docker():
    """
    Custom error when docker is not accessible
    """
    error('could not access the docker deamon')


def error_config():
    """
    Custom error when configuration is not accessible or when you can't
    create it
    """
    error('could not access or create configuration file')
