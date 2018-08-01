import docker as dockerpy
from tmn import display

VOLUMES = ['mastenode']
NETWORKS = ['mastenode']

# state
is_docker = False

# docker
_client = dockerpy.from_env()


def _ping():
    """
    Try to ping the Docker deamon. Check if accessible.

    :returns: is Docker running
    :rtype: bool
    """
    try:
        return _client.ping()
    except Exception:
        return False


def _create_volumes():
    for volume in VOLUMES:
        display.step_start_masternode_volume(volume)
        try:
            _client.volumes.get('masternode')
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.volumes.create('masternode')
            display.step_close_created()
        except dockerpy.errors.APIError:
            display.error_docker()


def _create_network():
    for network in NETWORKS:
        display.step_start_masternode_network(network)
        try:
            _client.networks.get('masternode')
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.networks.create('masternode')
            display.step_close_created()
        except dockerpy.errors.APIError:
            display.error_docker()


def start():
    _create_volumes()
    _create_network()


if _ping():
    is_docker = True
