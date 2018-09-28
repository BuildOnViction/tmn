import logging

import docker

logger = logging.getLogger('tmn')


class Network:
    """docstring for Network."""

    def __init__(self, client: docker.DockerClient, name: str) -> None:
        self.name = name
        self.network = None
        self.client = client
        try:
            self.network = self.client.networks.get(self.name)
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
                self.client.networks.create(self.name)
                return True
        except docker.errors.APIError as e:
            logger.error(e)
        except docker.errors.ConnectionRefusedError as e:
            logger.error(e)

    def remove(self) -> bool:
        "delete docker network"
        try:
            if self.network:
                self.network.remove()
                self.network = None
                return True
            else:
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False
