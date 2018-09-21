from typing import Dict, Union

import docker


class Service:
    """docstring for Service."""

    def __init__(
        self,
        image: str,
        name: str,
        hostname: str = None,
        network: str = None,
        environment: Dict[str] = {},
        volumes: Dict[Dict] = {},
        ports: Dict[Dict] = {},
        docker_url: str = None
    ) -> None:
        self.image = {'image': image}
        self.name = {'name': name}
        self.environment = {'environment': environment}
        self.network = network
        self.volumes = volumes
        self.ports = ports
        self.hostname = hostname
        self.detach = {'detach': True}
        if not docker_url:
            self._client = docker.from_env()
        else:
            self._client = docker.DockerClient(base_url=docker_url)
        try:
            self.container = docker.containers.get(self.name)
        except docker.errors.NotFound:
            pass
        except docker.errors.APIError:
            pass

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
                self.client.container.create(
                    image=self.image,
                    name=self.name,
                    hostname=self.hostname,
                    network=self.network,
                    environment=self.environment,
                    volumes=self.volumes
                )
                return True
        except docker.errors.APIError:
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
        except docker.errors.APIError:
            return False

    def status(self) -> Union[str, bool]:
        "return the status of the service container"
        try:
            if self.container:
                self.container.reload()
                return self.container.status
            else:
                return 'absent'
        except docker.errors.APIError:
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
        except docker.errors.APIError:
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
                return False
        except docker.errors.APIError:
            return False

    def remove(self) -> bool:
        "stop the service container"
        try:
            if self.container:
                self.container.remove(force=True)
                return True
            else:
                return True
        except docker.errors.APIError:
            return False
