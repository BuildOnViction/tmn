import pytest


@pytest.fixture
def test_data():
    from tmn import compose
    compose.volumes = ['test']
    compose.networks = ['test']
    compose.environment = {'TEST': 'test'}
    compose.containers = {
        'alpine1': {
            'image': 'alpine:latest',
            'name': 'test',
            'command': 'sleep 1000',
            'environment': None,
            'detach': True
        },
        'alpine2': {
            'image': 'alpine:latest',
            'name': 'test2',
            'command': 'sleep 1000',
            'environment': {'TEST': None, 'ALONE': None},
            'detach': True
        }
    }
    return compose


def test_process(test_data):
    test_data.process()
    assert test_data.containers['alpine1']['environment'] is None
    assert test_data.containers['alpine2']['environment']['TEST'] == 'test'
