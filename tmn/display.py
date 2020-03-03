import sys

import pastel

pastel.add_style('hg', 'green')
pastel.add_style('hgb', 'green', options=['bold'])
pastel.add_style('hy', 'yellow')
pastel.add_style('hyb', 'yellow', options=['bold'])
pastel.add_style('link', 'yellow', options=['underscore'])
pastel.add_style('und', options=['underscore'])
pastel.add_style('warning', 'yellow')
pastel.add_style('error', 'red')

help_url = 'https://docs.tomochain.com/masternode/tmn/'


def newline(number: int = 1) -> None:
    "Print newlines"
    print('\n'*number, end='')


def style(function):
    "Print and colorize strings with `pastel`"
    def wrapper(*args, **kwargs) -> None:
        print(pastel.colorize(function(*args, **kwargs)))
    return wrapper


def style_no_new_line(function):
    "Print and colorize strings with `pastel`. No newline."
    def wrapper(*args) -> None:
        print(pastel.colorize(function(*args)), end='', flush=True)
    return wrapper


@style
def link(msg: str, url: str) -> str:
    "Return a pastel formated string for browser links"
    return '<hg>{msg}</hg> <link>{url}</link>'.format(
        msg=msg,
        url=url
    )


def link_docs() -> None:
    "Custom link message for documentation"
    link('Documentation on running a masternode:', help_url)


@style
def title(msg: str) -> str:
    "Return a pastel formated title string"
    return '<hg>{msg}</hg>\n'.format(
        msg=msg
    )


def title_start_masternode(name: str) -> None:
    "Title when starting a masternode"
    title('Starting masternode <hy>{}</hy>:'.format(name))


def title_stop_masternode(name: str) -> None:
    "Title when stopping a masternode"
    title('Stopping masternode <hy>{}</hy>:'.format(name))


def title_status_masternode(name: str) -> None:
    "Title when viewing a masternode status"
    title('Masternode <hy>{}</hy> status:'.format(name))


def title_inspect_masternode(name: str) -> None:
    "Title when inspecting a masternode"
    title('Masternode <hy>{}</hy> details:'.format(name))


def title_update_masternode(name: str) -> None:
    "Title when updating a masternode"
    title('Updating masternode <hy>{}</hy>:'.format(name))


def title_remove_masternode(name: str) -> None:
    "Title when removing a masternode"
    title('Removing masternode <hy>{}</hy>:'.format(name))


@style
def subtitle(msg: str) -> str:
    "Return a pastel formated subtitle string"
    return '<und>{msg}</und>\n'.format(
        msg=msg
    )


def subtitle_create_volumes() -> None:
    "Subtitle when creating volumes"
    subtitle('Volumes')


def subtitle_remove_volumes() -> None:
    "Subtitle when removing volumes"
    subtitle('Volumes')


def subtitle_create_networks() -> None:
    "Subtitle when creating networks"
    subtitle('Networks')


def subtitle_remove_networks() -> None:
    "Subtitle when removing networks"
    subtitle('Networks')


def subtitle_create_containers() -> None:
    "Subtitle when creating containers"
    subtitle('Containers')


def subtitle_remove_containers() -> None:
    "Subtitle when removing containers"
    subtitle('Containers')


@style
def detail(msg, content: str, indent: int = 1) -> str:
    "Return a pastel formated detail"
    return ('  '*indent
            + '{msg}:\n'.format(msg=msg)
            + '  '*indent
            + '<hy>{content}</hy>'.format(content=content))


def detail_identity(content: str) -> None:
    "Custom detail message for the masternode identity"
    detail('Unique identity', content)


def detail_coinbase(content: str) -> None:
    "Custom detail message for the masternode coinbase address"
    detail('Coinbase address (account public key)', content)


@style_no_new_line
def step(msg: str, indent: int = 1) -> str:
    "Return a pastel formated step with indentation."
    step = '  '*indent + '- {msg}... '.format(
        msg=msg
    )
    return step


def step_create_volume(name: str) -> None:
    "Custom step message for docker volumes creation"
    step('Creating <hy>{name}</hy>'.format(
        name=name
    ))


def step_remove_volume(name: str) -> None:
    "Custom step message for docker volumes removal"
    step('Removing <hy>{name}</hy>'.format(
        name=name
    ))


def step_create_network(name: str) -> None:
    "Custom step message for docker networks creation"
    step('Creating <hy>{name}</hy>'.format(
        name=name
    ))


def step_remove_network(name: str) -> None:
    "Custom step message for docker networks creation"
    step('Removing <hy>{name}</hy>'.format(
        name=name
    ))


def step_create_container(name: str) -> None:
    "Custom step message for docker container creation"
    step('Creating <hy>{name}</hy>'.format(
        name=name
    ))


def step_start_container(name: str) -> None:
    "Custom step message for docker container starting"
    step('Starting <hy>{name}</hy>'.format(
        name=name
    ))


def step_remove_container(name: str) -> None:
    "Custom step message for docker container starting"
    step('Removing <hy>{name}</hy>'.format(
        name=name
    ))


def step_stop_container(name: str) -> None:
    "Custom step message for docker container stopping"
    step('Stopping <hy>{name}</hy>'.format(
        name=name
    ))


@style
def step_close(msg: str, color: str = 'green') -> str:
    "Return a pastel formated end of step"
    return '<fg={color}>{msg}</>'.format(
        msg=msg,
        color=color
    )


def step_close_ok() -> None:
    "Custom close message when all ok"
    msg = 'ok'
    if sys.stdout.encoding == 'UTF-8':
        msg = '✔'
    step_close(msg)


def step_close_nok() -> None:
    "Custom close message when all ok"
    msg = 'error'
    if sys.stdout.encoding == 'UTF-8':
        msg = '✗'
    step_close(msg, 'red')


@style
def status(name: str = '', status: str = 'absent', id: str = '',
           status_color: str = 'red') -> str:
    "Return a pastel formated end of step"
    if id:
        return '  {name}\t<fg={color}>{status}(</>{id}<fg={color}>)</>'.format(
            name=name,
            status=status,
            color=status_color,
            id=id
        )
    else:
        return '  {name}\t<fg={color}>{status}</>'.format(
            name=name,
            status=status,
            color=status_color,
        )


@style
def warning(msg: str, newline: bool = True) -> str:
    "Return a pastel formated string for warnings"
    before = ''
    if newline:
        before = '\n'
    return before + '<warning>! warning:</warning> {msg}\n'.format(
        msg=msg
    )


def warning_ignoring_start_options(name: str) -> None:
    "Custom warning when tmn is ignoring the start options"
    warning(
        'masternode <hy>{}</hy> is already configured\n'.format(name)
        + '           '
        + 'ignoring start options\n'
    )


def warning_remove_masternode(name: str) -> None:
    "Custom warning when tmn is removing masternode but no confirmation"
    warning(
        'you are about to remove masternode <hy>{}</hy>\n'.format(name)
        + '           '
        + 'this will permanently delete its data\n'
        + '           '
        + 'to confirm use the <hy>--confirm</hy> flag'
    )


@style
def error(msg: str) -> str:
    "Return a pastel formated string for errors"
    return (
        '\n<error>! error:</error> {msg}\n'.format(msg=msg)
        + '         '
        + 'need help? <hy>{}</hy>'.format(help_url)
    )


def error_docker() -> None:
    "Custom error when docker is not accessible"
    error('could not access the docker daemon')


def error_docker_api() -> None:
    "Custom error when docker is not accessible"
    error('something went wrong while doing stuff with docker')


def error_start_not_initialized() -> None:
    "Custom error when `tmn start` has never been used with `--name` option"
    error(
        'tmn doesn\'t manage any masternode yet\n'
        '         please use '
        '<hy>tmn start --name</hy> to get started'
    )


def error_start_option_required(option: str) -> None:
    "Custom error when `tmn start` is used with name but not the other options"
    error(
        '<hy>{}</hy> is required when starting a new masternode'
        .format(option)
    )


def error_validation_option(option: str, format: str) -> None:
    "Custom error when an option format is not valide"
    error(
        '<hy>{}</hy> is not valid\n'.format(option)
        + '         it should be a {}'.format(format)
    )


def error_breaking_change() -> None:
    "Custom error when breaking changes need to recreate the node"
    error(
        'latest update introduced some non-retrocompatible changes\n'
        '         '
        'please recreate your node by deleting it\n'
        '         '
        '<hy>tmn remove --confirm</hy>\n'
        '         '
        'and creating it back with the same options as the old one\n'
        '         '
        '<hy>tmn start --name ... --net ... --pkey ...</hy>'
    )
