import pastel

pastel.add_style('hg', 'green')
pastel.add_style('hgb', 'green', options=['bold'])
pastel.add_style('hy', 'yellow')
pastel.add_style('hyb', 'yellow', options=['bold'])
pastel.add_style('link', 'yellow', options=['underscore'])
pastel.add_style('und', options=['underscore'])
pastel.add_style('warning', 'yellow')
pastel.add_style('error', 'red')

help_url = 'https://docs.tomochain.com/'


def newline(number=1):
    """
    Print newlines

    :param number: the number of newlines to print
    :type number: int
    """
    print('\n'*number, end='')


def style(function):
    """
    Print and colorize strings with `pastel`

    :param function: function to decorate
    :type function: function
    :returns: decorated function
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        print(pastel.colorize(function(*args, **kwargs)))
    return wrapper


def style_no_new_line(function):
    """
    Print and colorize strings with `pastel`. Don't add a new line at the end.

    Decorator to print and colorize strings with `pastel`.
    Don't add a new line at the end.

    :param function: function to decorate
    :type function: function
    :returns: decorated function
    :rtype: function
    """
    def wrapper(*args):
        print(pastel.colorize(function(*args)), end='', flush=True)
    return wrapper


@style
def link(msg, url):
    """
    Return a pastel formated string for browser links

    :param msg: message
    :type msg: str
    :param url: website url
    :type url: str
    """
    return '<hg>{msg}</hg> <link>{url}</link>'.format(
        msg=msg,
        url=url
    )


def link_docs():
    """
    Custom link message for documentation
    """
    link('Documentation on running a masternode:', help_url)


@style
def title(msg):
    """
    Return a pastel formated title string

    :param msg: title message
    :type msg: str
    :returns: subtitle formated
    :rtype: str
    """
    return '<hg>{msg}</hg>\n'.format(
        msg=msg
    )


def title_start_masternode(name):
    """
    Title when starting a masternode
    """
    title('Starting masternode <hy>{}</hy>:'.format(name))


def title_stop_masternode(name):
    """
    Title when stopping a masternode
    """
    title('Stopping masternode <hy>{}</hy>:'.format(name))


def title_status_masternode(name):
    """
    Title when stopping a masternode
    """
    title('Masternode <hy>{}</hy> status:'.format(name))


def title_inspect_masternode(name):
    """
    Title when stopping a masternode
    """
    title('Masternode <hy>{}</hy> details:'.format(name))


def title_remove_masternode(name):
    """
    Title when stopping a masternode
    """
    title('Removing masternode <hy>{}</hy>:'.format(name))


@style
def subtitle(msg):
    """
    Return a pastel formated subtitle string

    :param msg: subtitle message
    :type msg: str
    :returns: subtitle formated
    :rtype: str
    """
    return '<und>{msg}</und>\n'.format(
        msg=msg
    )


def subtitle_create_volumes():
    """
    Subtitle when creating volumes
    """
    subtitle('Volumes')


def subtitle_remove_volumes():
    """
    Subtitle when removing volumes
    """
    subtitle('Volumes')


def subtitle_create_networks():
    """
    Subtitle when creating networks
    """
    subtitle('Networks')


def subtitle_remove_networks():
    """
    Subtitle when removing networks
    """
    subtitle('Networks')


def subtitle_create_containers():
    """
    Subtitle when creating containers
    """
    subtitle('Containers')


def subtitle_remove_containers():
    """
    Subtitle when removing containers
    """
    subtitle('Containers')


@style
def detail(msg, content, indent=1):
    """
    Return a pastel formated detail

    :param msg: detail message
    :type msg: str
    :param content: detail content
    :type content: str
    :returns: `msg` formated
    :rtype: str
    """
    return ('  '*indent
            + '{msg}:\n'.format(msg=msg)
            + '  '*indent
            + '<hy>{content}</hy>'.format(content=content))


def detail_identity(content):
    """
    Custom detail message for the masternode identity
    """
    detail('Unique identity', content)


def detail_coinbase(content):
    """
    Custom detail message for the masternode coinbase address
    """
    detail('Coinbase address (account public key)', content)


@style_no_new_line
def step(msg, indent=1):
    """
    Return a pastel formated step with indentation.
    One indent is two spaces.

    :param msg: step message
    :type msg: str
    :param indent: number of idents
    :type indent: int
    :returns: `msg` formated
    :rtype: str
    """
    step = '  '*indent + '- {msg}... '.format(
        msg=msg
    )
    return step


def step_create_masternode_volume(volume):
    """
    Custom step message for docker volumes creation
    """
    step('Creating <hy>{volume}</hy>'.format(
        volume=volume
    ))


def step_remove_masternode_volume(volume):
    """
    Custom step message for docker volumes removal
    """
    step('Removing <hy>{volume}</hy>'.format(
        volume=volume
    ))


def step_create_masternode_network(network):
    """
    Custom step message for docker networks creatin
    """
    step('Creating <hy>{network}</hy>'.format(
        network=network
    ))


def step_remove_masternode_network(network):
    """
    Custom step message for docker networks creatin
    """
    step('Removing <hy>{network}</hy>'.format(
        network=network
    ))


def step_create_masternode_container(container):
    """
    Custom step message for docker container creation
    """
    step('Creating <hy>{container}</hy>'.format(
        container=container
    ))


def step_start_masternode_container(container):
    """
    Custom step message for docker container starting
    """
    step('Starting <hy>{container}</hy>'.format(
        container=container
    ))


def step_remove_masternode_container(container):
    """
    Custom step message for docker container starting
    """
    step('Removing <hy>{container}</hy>'.format(
        container=container
    ))


def step_stop_masternode_container(container):
    """
    Custom step message for docker container stopping
    """
    step('Stopping <hy>{container}</hy>'.format(
        container=container
    ))


@style
def step_close(msg, color='green'):
    """
    Return a pastel formated end of step

    :param msg: task status of the step
    :type msg: str
    :returns: `msg` formated
    :rtype: str
    """
    return '<fg={color}>{msg}</>'.format(
        msg=msg,
        color=color
    )


# TODO only use step_close_status
def step_close_created():
    """
    Custom 'created' closing step message
    """
    step_close('created')


def step_close_exists():
    """
    Custom 'exists' closing step message
    """
    step_close('exists')


def step_close_status(status):
    """
    Custom 'status' closing step message
    """
    step_close(status)


@style
def status(name='', status='absent', id='', status_color='red'):
    """
    Return a pastel formated end of step

    :param msg: task status of the step
    :type msg: str
    :returns: `msg` formated
    :rtype: str
    """
    if id:
        return '  {name}\t<fg={color}>{status}(</>{id}<fg={color}>)</>'.format(
            name=name,
            status=status,
            color=status_color,
            id=id
        )
    else:
        return '  {name}\t<fg={color}>{status}{id}</>'.format(
            name=name,
            status=status,
            color=status_color,
            id=id
        )


@style
def warning(msg, newline=True):
    """
    Return a pastel formated string for warnings

    :param msg: error message
    :type msg: str
    :returns: `msg` formated
    :rtype: str
    """
    before = ''
    if newline:
        before = '\n'
    return before + '<warning>! warning:</warning> {msg}\n'.format(
        msg=msg
    )


def warning_ignoring_start_options(name):
    """
    Custom warning when tmn is ignoring the start options
    """
    warning(
        'masternode <hy>{}</hy> is already configured\n'.format(name)
        + '           '
        + 'ignoring start options\n'
    )


def warning_nothing_to_remove():
    """
    Custom warning when tmn is removing docker objects but it's empty
    """
    warning(
        'nothing to remove', newline=False
    )


def warning_remove_masternode(name):
    """
    Custom warning when tmn is removing masternode but no confirmation
    """
    warning(
        'you are about to remove masternode <hy>{}</hy>\n'.format(name)
        + '           '
        + 'this will permanently delete its data\n'
        + '           '
        + 'to confirm use the <hy>--confirm</hy> flag'
    )


@style
def error(msg):
    """
    Return a pastel formated string for errors

    :param msg: error message
    :type msg: str
    :returns: `msg` formated
    :rtype: str
    """
    return (
        '\n<error>! error:</error> {msg}\n'.format(msg=msg)
        + '         '
        + 'need help? <hy>{}</hy>'.format(help_url)
    )


def error_docker():
    """
    Custom error when docker is not accessible
    """
    error('could not access the docker daemon')


def error_docker_api():
    """
    Custom error when docker is not accessible
    """
    error('something went wrong while doing stuff with docker')


def error_start_not_initialized():
    """
    Custom error when `tmn start` has never been used with the `--name` option
    """
    error(
        'tmn doesn\'t manage any masternode yet\n'
        '         please use '
        '<hy>tmn start --name</hy> to get started'
    )


def error_start_option_required(option):
    """
    Custom error when `tmn start` is used with name but not the other options
    """
    error(
        '<hy>{}</hy> is required when starting a new masternode'
        .format(option)
    )


def error_validation_option(option, format):
    """
    Custom error when an option format is not valide
    """
    error(
        '<hy>{}</hy> is not valid\n'.format(option)
        + '         it should be a {}'.format(format)
    )
