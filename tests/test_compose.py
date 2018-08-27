import pytest


@pytest.fixture
def test_data():
    from tmn import compose
    compose.environment = {'PRIVATE_KEY': 'test'}
    compose.containers['test'] = {
        'image': 'test',
        'hostname': None,
        'name': 'test',
        'environment': {},
        'network': 'tmn_default',
        'volumes': {},
        'detach': True
    }
    return compose


def test_process(test_data):
    test_data.process('test')
    assert 'test_' in test_data.containers['metrics']['hostname']
    assert len(test_data.containers['metrics']['hostname']) == 11
    assert 'test_' in (
        test_data.containers['tomochain']['environment']['IDENTITY'])
    assert test_data.containers['tomochain']['environment']['PRIVATE_KEY'] == (
        'test')
