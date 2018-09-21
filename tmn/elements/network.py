import docker


class Network:
    """docstring for Network."""

    def __init__(self, name: str, docker_url: str = None):
        self.name = name
        if not docker_url:
            self._client = docker.from_env()
        else:
            self._client = docker.DockerClient(base_url=docker_url)

    def create(self) -> bool:
        "create docker network"
        try:
            try:
                self._client.networks.get(self.name)
                return True
            except docker.errors.NotFound:
                self._client.networks.create(self.name)
                return True
        except docker.errors.APIError:
            return False

    def delete(self) -> bool:
        "delete docker network"
        try:
            try:
                n = self._client.networks.get(self.name)
                n.remove()
                return True
            except docker.errors.NotFound:
                return True
        except docker.errors.APIError:
            return False
