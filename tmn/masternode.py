import docker as dockerpy

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


def start():
    pass


if _ping():
    is_docker = True
