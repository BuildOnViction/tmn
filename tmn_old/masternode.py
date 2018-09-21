import sys
import docker as dockerpy
from tmn import compose
from tmn import display
from tmn import configuration

_client = None


def apierror(function):
    """
    Decorator to catch `docker.errors.APIerror` Exception

    :param function: function to decorate
    :type function: function
    :returns: decorated function
    :rtype: function
    """
    def wrapper(*args, **kwargs):
        try:
            function(*args, **kwargs)
        except dockerpy.errors.APIError:
            display.error_docker_api()
            sys.exit()
    return wrapper


def connect(url=None):
    """
    Create the docker client. Try to ping the docker server to establish if
    the connexion in successful

    :param url: url to the docker deamon
    :type url: str
    :returns: is connected to Docker api
    :rtype: bool
    """
    global _client
    if not url:
        _client = dockerpy.from_env()
    else:
        _client = dockerpy.DockerClient(base_url=url)
    return _ping()


def _ping():
    """
    Try to ping the Docker daemon. Check if accessible.

    :returns: is Docker api reachable
    :rtype: bool
    """
    try:
        return _client.ping()
    except Exception:
        return False


def _create_volumes():
    """
    Try to get the volumes defined in `compose.volumes`.
    If it fails, create them.
    """
    for volume in compose.volumes:
        display.step_create_masternode_volume(volume)
        try:
            _client.volumes.get(volume)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.volumes.create(volume)
            display.step_close_created()
    display.newline()


def _remove_volumes():
    """
    Remove Volumes
    """
    for volume in compose.volumes:
        display.step_remove_masternode_volume(volume)
        try:
            v = _client.volumes.get(volume)
            v.remove(force=True)
            display.step_close_status('removed')
        except dockerpy.errors.NotFound:
            display.step_close_status('absent')
    display.newline()


def _create_networks():
    """
    Try to get the networks defined in `compose.networks`.
    If it fails, create them.
    """
    for network in compose.networks:
        display.step_create_masternode_network(network)
        try:
            _client.networks.get(network)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.networks.create(network)
            display.step_close_created()
    display.newline()


def _remove_networks():
    """
    Remove networks
    """
    for network in compose.networks:
        display.step_remove_masternode_network(network)
        try:
            n = _client.networks.get(network)
            n.remove()
            display.step_close_status('removed')
        except dockerpy.errors.NotFound:
            display.step_close_status('absent')
    display.newline()


def _get_existing_containers():
    """
    Get from docker the containers defined in `compose.containers`.

    :returns: The existing `docker.Container`
    :rtype: list
    """
    containers = {}
    for key, value in compose.containers.items():
        try:
            container = _client.containers.get(value['name'])
            containers[container.name] = container
        except dockerpy.errors.NotFound:
            pass
    return containers


def _create_containers():
    """
    Try to get the containers defined in `compose.containers`.
    If it fails, create them.

    :returns: The created or existing `docker.Container`
    :rtype: list
    """
    containers = {}
    for key, value in compose.containers.items():
        display.step_create_masternode_container(value['name'])
        try:
            container = _client.containers.get(value['name'])
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            # temporary, see https://github.com/docker/docker-py/issues/2101
            _client.images.pull(value['image'])
            container = _client.containers.create(**value)
            display.step_close_created()
        containers[container.name] = container
    return containers


def _start_containers(containers):
    """
    Verify the container status. If it's not restarting or running,
    start them.

    :param containers: dict of name:`docker.Container`
    :type containers: dict
    """
    for name, container in containers.items():
        display.step_start_masternode_container(container.name)
        container.reload()
        # filtered status are:
        # created|restarting|running|removing|paused|exited|dead
        # might have to add all the status
        if container.status in ['restarting', 'running']:
            pass
        elif container.status in ['paused']:
            container.unpause()
        elif container.status in ['created', 'exited', 'dead']:
            container.start()
        container.reload()
        display.step_close_status(container.status)


def _remove_containers(containers):
    """
    Remove given containers

    :param containers: dict of name:`docker.Container`
    :type containers: dict
    """
    if not containers:
        display.warning_nothing_to_remove()
    else:
        display.newline()
    for name, container in containers.items():
        display.step_remove_masternode_container(container.name)
        container.remove(force=True)
        display.step_close_status('removed')
    if containers:
        display.newline()


def _stop_containers(containers):
    """
    Stop the given dict of `docker.Container`

    :param containers: dict of name:`docker.Container`
    :type containers: dict
    """
    for name, container in containers.items():
        display.step_stop_masternode_container(container.name)
        container.reload()
        # filtered status are:
        # created|restarting|running|removing|paused|exited|dead
        # might have to add all the status
        if container.status in ['restarting', 'running', 'paused']:
            container.stop()
        elif container.status in ['created', 'exited', 'dead']:
            pass
        container.reload()
        display.step_close_status(container.status)


def _status_containers(containers):
    """
    Display the status of `CONTAINERS` w/ the passed list of `docker.Container`

    :param containers: dict of `docker.Container`
    :type containers: dict
    """
    names = [
        compose.containers[container]['name']
        for container in list(compose.containers)
    ]
    for name in names:
        display_kwargs = {}
        display_kwargs.update({'name': name})
        try:
            containers[name].reload()
            if containers[name].status in ['running']:
                display_kwargs.update({'status_color': 'green'})
            display_kwargs.update({'status': containers[name].status})
            display_kwargs.update({'id': containers[name].short_id})
        except KeyError:
            display_kwargs.update({'name': name})
            display_kwargs.update({'name': name})
        display.status(**display_kwargs)


def _get_coinbase():
    """
    Retrieve the coinbase address from the account used by the masternode

    :returns: coinbase address
    :rtype: str
    """
    container = _client.containers.get(compose.containers['tomochain']['name'])
    return '0x' + container.exec_run(
        'tomo account list --keystore keystore'
    ).output.decode("utf-8").replace('}', '{').split("{")[1]


def _get_identity():
    """
    Retrieve the masternode identity

    :returns: identity
    :rtype: str
    """
    container = _client.containers.get(compose.containers['tomochain']['name'])
    return container.exec_run(
        '/bin/sh -c "echo $IDENTITY"'
    ).output.decode("utf-8")


@apierror
def start(name):
    """
    Start a masternode. Includes:
    - process components
    - creating volumes
    - creating networks
    - creating containers
    - starting containers

    :param name: name of the masternode
    :type name: str
    """
    compose.process(name)
    display.subtitle_create_volumes()
    _create_volumes()
    display.subtitle_create_networks()
    _create_networks()
    display.subtitle_create_containers()
    containers = _create_containers()
    display.newline()
    _start_containers(containers)


@apierror
def stop(name):
    """
    Stop a masternode. Includes:
    - process components
    - getting the list of containers
    - stoping them

    :param name: name of the masternode
    :type name: str
    """
    compose.process(name)
    containers = _get_existing_containers()
    _stop_containers(containers)


@apierror
def status(name):
    """
    Retrieve masternode status. Includes:
    - process components
    - getting the list of containers
    - displaying their status

    :param name: name of the masternode
    :type name: str
    """
    compose.process(name)
    containers = _get_existing_containers()
    _status_containers(containers)


@apierror
def remove(name):
    """
    Remove masternode. Includes:
    - process components
    - stop containers
    - remove containers, networks and volumes
    - remove tmn persistent configuration

    :param name: name of the masternode
    :type name: str
    """
    compose.process(name)
    containers = _get_existing_containers()
    display.subtitle_remove_containers()
    _stop_containers(containers)
    _remove_containers(containers)
    display.subtitle_remove_networks()
    _remove_networks()
    display.subtitle_remove_volumes()
    _remove_volumes()
    configuration.remove_conf('name')
    configuration.remove_conf('identity')


@apierror
def details(name):
    """
    Remove masternode. Includes:
    - process components
    - stop containers
    - remove containers, networks and volumes
    - remove tmn persistent configuration

    :param name: name of the masternode
    :type name: str
    """
    compose.process(name)
    display.detail_identity(_get_identity())
    display.detail_coinbase(_get_coinbase())
