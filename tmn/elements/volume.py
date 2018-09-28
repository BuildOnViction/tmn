import logging

import docker

logger = logging.getLogger('tmn')


class Volume:
    """docstring for Volume."""

    def __init__(self, client: docker.DockerClient, name: str) -> None:
        self.name = name
        self.volume = None
        self.client = client
        try:
            self.volume = self.client.volumes.get(self.name)
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
                self.client.volumes.create(self.name)
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def remove(self) -> bool:
        "delete docker volume"
        try:
            if self.volume:
                self.volume.remove(force=True)
                self.volume = None
                return True
            else:
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False
