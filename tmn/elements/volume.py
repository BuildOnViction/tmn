import logging

import docker

logger = logging.getLogger('tmn')


class Volume:
    """docstring for Volume."""

    def __init__(self, name: str, docker_url: str = None) -> None:
        self.name = name
        self.volume = None
        if not docker_url:
            self._client = docker.from_env()
        else:
            self._client = docker.DockerClient(base_url=docker_url)
        try:
            self.volume = self._client.volumes.get(self.name)
        except docker.errors.NotFound as e:
            logger.debug('volume {} not yet created ({})'
                         .format(self.name, e))
        except docker.errors.APIError as e:
            logger.error(e)

    def create(self) -> bool:
        "create docker volumes"
        try:
            if self.volume:
                return True
            else:
                self._client.volumes.create(self.name)
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def remove(self) -> bool:
        "delete docker volume"
        try:
            if self.volume:
                self.volume.remove(force=True)
                return True
            else:
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False
