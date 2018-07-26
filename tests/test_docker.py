import pytest
import docker as dockerpy
from tmn.docker import DockerManager


@pytest.fixture
def docker_client():
    manager = DockerManager()
    manager.client = dockerpy.from_env()
    return manager


@pytest.fixture
def docker_client_fail():
    manager = DockerManager()
    manager.client = dockerpy.DockerClient(base_url='unix://wrong')
    return manager


def test_instance():
    assert isinstance(DockerManager(), DockerManager)


def test_ping_success(docker_client):
    assert docker_client.ping()


def test_ping_fail(docker_client_fail):
    assert not docker_client_fail.ping()
