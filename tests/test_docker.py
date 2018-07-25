import docker as dockerpy
from tmn.docker import DockerManager


def test_instance():
    assert isinstance(DockerManager(), DockerManager)


def test_ping_fail():
    manager = DockerManager()
    manager.client = dockerpy.DockerClient(base_url='unix://wrong')
    assert not manager.ping()
