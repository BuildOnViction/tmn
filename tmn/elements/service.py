import logging
from typing import Dict, Union

import docker

logger = logging.getLogger('tmn')


class Service:
    """docstring for Service."""

    def __init__(
        self,
        client: docker.DockerClient,
        name: str,
        image: str = None,
        hostname: str = None,
        network: str = None,
        environment: Dict[str, str] = {},
        volumes: Dict[str, Dict[str, str]] = {},
        ports: Dict[str, Dict[str, str]] = {},
        log_driver: str = 'json-file',
        log_opts: Dict[str, str] = {'max-size': '3g'}
    ) -> None:
        self.container = False
        self.image = image
        self.name = name
        self.environment = environment
        self.network = network
        self.hostname = hostname
        self.volumes = volumes
        self.ports = ports
        self.log_driver = log_driver
        self.log_opts = log_opts
        self.client = client
        try:
            self.container = self.client.containers.get(self.name)
        except docker.errors.NotFound as e:
            logger.debug('container {} not yet created ({})'
                         .format(self.name, e))
        except docker.errors.APIError as e:
            logger.error(e)

    def add_environment(self, name: str, value: str) -> None:
        "add a new environment to the service"
        self.environment[name] = value

    def add_volume(self, source: str, target: str, mode: str = 'rw') -> None:
        "add a new volume to the service"
        self.volumes[source] = {'bind': target, 'mode': mode}

    def add_port(self, source: str, target: str) -> None:
        "add a new port mapping to the service"
        self.ports[source] = target

    def create(self) -> bool:
        "create the service container"
        try:
            if self.container:
                return True
            else:
                self.client.images.pull(self.image)
                self.container = self.client.containers.create(
                    image=self.image,
                    name=self.name,
                    hostname=self.hostname,
                    network=self.network,
                    environment=self.environment,
                    volumes=self.volumes,
                    log_config={'type': self.log_driver,
                                'config': self.log_opts},
                    detach=True
                )
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def start(self) -> bool:
        "start the service container"
        try:
            if self.container:
                self.container.reload()
                if self.container.status in ['running', 'restarting']:
                    return True
                elif self.container.status in ['paused']:
                    self.container.unpause()
                    return True
                else:
                    self.container.start()
                    return True
            else:
                return False
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def status(self) -> Union[str, bool]:
        "return the status of the service container"
        try:
            if self.container:
                self.container.reload()
                return self.container.status
            else:
                return 'absent'
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def execute(self, command: str) -> Union[str, bool]:
        "return the result of a command on the service container"
        try:
            if self.container:
                self.container.reload()
                return self.container.exec_run(
                    '/bin/sh -c "{}"'.format(command)
                ).output.decode("utf-8")
            else:
                return False
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def stop(self) -> bool:
        "stop the service container"
        try:
            if self.container:
                self.container.reload()
                if self.container.status in ['created', 'exited', 'dead']:
                    return True
                else:
                    self.container.stop()
                    return True
            else:
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def remove(self) -> bool:
        "stop the service container"
        try:
            if self.container:
                self.container.remove(force=True)
                self.container = None
                return True
            else:
                return True
        except docker.errors.APIError as e:
            logger.error(e)
            return False

    def update(self) -> bool:
        "update the service container"
        try:
            if self.container:
                self.container.remove(force=True)
                return self.create() and self.start()
            else:
                return False
        except docker.errors.APIError as e:
            logger.error(e)
            return False
