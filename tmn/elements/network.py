import logging

import docker

logger = logging.getLogger('tmn')


class Network:
    """docstring for Network."""

    def __init__(self, name: str, docker_url: str = None):
        self.name = name
        self.network = None
        if not docker_url:
            self._client = docker.from_env()
        else:
            self._client = docker.DockerClient(base_url=docker_url)
        try:
            self.network = self._client.networks.get(self.name)
        except docker.errors.NotFound as e:
            logger.debug('network {} not yet created ({})'
                         .format(self.name, e))
        except docker.errors.APIError as e:
            logger.error(e)

    def create(self) -> bool:
        "create docker network"
        try:
            if self.network:
                return True
            else:
                self._client.networks.create(self.name)
                return True
        except docker.errors.APIError as e:
            logger.error(e)

    def remove(self) -> bool:
        "delete docker network"
        try:
            if self.network:
                self.volume.remove()
                return True
            else:
                return True
        except docker.errors.APIError as e:
            logger.error(e)
