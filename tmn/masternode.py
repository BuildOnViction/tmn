import docker as dockerpy
from tmn import display

VOLUMES = ['blockchain_data']
NETWORKS = ['masternode']
CONTAINERS = {
    'telegraf': {
        'image': 'tomochain/infra-telegraf:devnet',
        'hostname': 'test',
        'name': 'telegraf',
        'network': NETWORKS[0],
        'volumes': {
            '/var/run/docker.sock': {
                'bind': '/var/run/docker.sock', 'mode': 'ro'
            },
            '/sys': {
                'bind': '/rootfs/sys', 'mode': 'ro'
            },
            '/proc': {
                'bind': '/rootfs/proc', 'mode': 'ro'
            },
            '/etc': {
                'bind': '/rootfs/etc', 'mode': 'ro'
            }
        },
        'detach': True
    },
    'tomochain': {
        'image': 'tomochain/infra-tomochain:devnet',
        'name': 'tomochain',
        'network': NETWORKS[0],
        'volumes': {
            VOLUMES[0]: {
                'bind': '/tomochain/data', 'mode': 'rw'
            }
        },
        'detach': True
    },
}

_client = dockerpy.from_env()
connected = False


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
            _client.volumes.get(volume)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.volumes.create(volume)
            display.step_close_created()
        except dockerpy.errors.APIError:
            display.error_docker()


def _create_network():
    for network in NETWORKS:
        display.step_start_masternode_network(network)
        try:
            _client.networks.get(network)
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.networks.create(network)
            display.step_close_created()
        except dockerpy.errors.APIError:
            display.error_docker()


def _create_containers():
    for container, config in CONTAINERS.items():
        display.step_start_masternode_container(config['name'])
        try:
            _client.containers.get(config['name'])
            display.step_close_exists()
        except dockerpy.errors.NotFound:
            _client.containers.create(**config)
            display.step_close_created()
        except dockerpy.errors.APIError:
            display.error_docker()


def start():
    _create_volumes()
    _create_network()
    _create_containers()


if _ping():
    connected = True
