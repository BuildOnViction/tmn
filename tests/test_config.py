import pytest
from tmn.config import ConfigManager


@pytest.fixture
def config(tmpdir):
    config = ConfigManager()
    return config


@pytest.fixture
def config_path(tmpdir):
    config = ConfigManager('/tmp/tmn')
    return config


def test_instance(config):
    assert isinstance(config, ConfigManager)


def test_init(config):
    assert config.valid


def test_init_path(config_path):
    assert config_path.valid
