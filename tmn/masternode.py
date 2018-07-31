from collections import namedtuple
import docker as dockerpy

# state
_State = namedtuple('State', 'NEW DOCKER_OK DOCKER_ERROR STARTING')
states = _State('NEW', 'DOCKER_OK', 'DOCKER_ERROR', 'STARTING')
state = states.NEW

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


def start():
    pass


if _ping():
    state = states.DOCKER_OK
