import docker


class Volume:
    """docstring for Volume."""

    def __init__(self, name: str, docker_url: str = None):
        self.name = name
        if not docker_url:
            self._client = docker.from_env()
        else:
            self._client = docker.DockerClient(base_url=docker_url)

    def create(self) -> bool:
        "create docker volumes"
        try:
            try:
                self._client.volumes.get(self.name)
                return True
            except docker.errors.NotFound:
                self._client.networks.create(self.network)
                return True
        except docker.errors.APIError:
            return False

    def remove(self) -> bool:
        "delete docker volume"
        try:
            try:
                v = self._client.volumes.get(self.name)
                v.remove(force=True)
                return True
            except docker.errors.NotFound:
                return True
        except docker.errors.APIError:
            return False
