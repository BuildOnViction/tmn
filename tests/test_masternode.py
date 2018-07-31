import pytest
import docker as dockerpy
from tmn import masternode


@pytest.fixture
def fail():
    masternode._client = dockerpy.DockerClient(base_url='unix://wrong')


def test_ping_success():
    assert masternode._ping()


def test_ping_fail(fail):
    assert not masternode._ping()
