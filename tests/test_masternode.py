import pytest
import docker as dockerpy
from tmn.masternode import Masternode


@pytest.fixture
def masternode_client():
    masternode = Masternode()
    masternode.client = dockerpy.from_env()
    return masternode


@pytest.fixture
def masternode_client_fail():
    masternode = Masternode()
    masternode.client = dockerpy.DockerClient(base_url='unix://wrong')
    return masternode


def test_instance():
    assert isinstance(Masternode(), Masternode)


def test_ping_success(masternode_client):
    assert masternode_client.ping()


def test_ping_fail(masternode_client_fail):
    assert not masternode_client_fail.ping()
