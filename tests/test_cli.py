import pytest
import tmn as package
from tmn import tmn

mn = 'test'
# le = len(mn)


@pytest.fixture
def runner():
    from click.testing import CliRunner
    runner = CliRunner()
    return runner


def test_version(runner):
    version = '0.0.4'
    result = runner.invoke(tmn.main, ['--version'])
    assert result.output[-6:-1] == version
    assert package.__version__ == version


def test_error_docker(runner):
    result = runner.invoke(tmn.main, ['--dockerurl', 'unix://test', 'docs'])
    assert '! error: could not access the docker daemon\nNone\n'
    assert result.exit_code != 0


def test_command(runner):
    result = runner.invoke(tmn.main)
    assert result.exit_code == 0


def test_command_docs(runner):
    result = runner.invoke(tmn.main, ['docs'])
    msg = 'Documentation on running a masternode:'
    link = 'https://docs.tomochain.com/\n'
    assert result.output == "{} {}".format(msg, link)
    assert result.exit_code == 0


def test_command_docs_opt_open(runner):
    result = runner.invoke(tmn.main, ['docs', '--open'])
    msg = 'Opening documentation:'
    link = 'https://docs.tomochain.com/\n'
    assert result.output == "{} {}".format(msg, link)
    assert result.exit_code == 0


def test_command_list(runner):
    result = runner.invoke(tmn.main, ['list'])
    lines = result.output.splitlines()
    assert lines[0] == 'Tomochain masternodes on this machine:'
    assert result.exit_code == 0


def test_command_list_arg(runner):
    result = runner.invoke(tmn.main, ['list', 'test'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2


def test_command_create(runner):
    result = runner.invoke(tmn.main, ['create', mn])
    lines = result.output.splitlines()
    assert lines[0] == 'Creating masternode {}!'.format(mn)
    assert result.exit_code == 0
    n = tmn.masternode._client.networks.get('{}_network'.format(mn))
    v = tmn.masternode._client.volumes.get('{}_data'.format(mn))
    for container in tmn.masternode._get_containers(name=mn):
        container.remove(force=True)
    n.remove()
    v.remove(force=True)


def test_command_create_no_arg(runner):
    result = runner.invoke(tmn.main, ['create'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2


def test_command_start(runner):
    c = {
        'image': 'alpine:latest',
        'name': '{}_{}'.format(mn, mn),
        'command': 'sleep 1000',
        'labels': {'tmn': mn},
        'detach': True
    }
    tmn.masternode._client.containers.create(**c)
    result = runner.invoke(tmn.main, ['start', mn])
    lines = result.output.splitlines()
    assert lines[0] == 'Starting masternode {}!'.format(mn)
    assert result.exit_code == 0
    for container in tmn.masternode._get_containers(name=mn):
        container.remove(force=True)


def test_command_start_empty(runner):
    result = runner.invoke(tmn.main, ['start', mn])
    lines = result.output.splitlines()
    assert lines[0] == 'Starting masternode {}!'.format(mn)
    assert 'error' in lines[2]
    assert result.exit_code == 0


def test_command_start_no_arg(runner):
    result = runner.invoke(tmn.main, ['start'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2


def test_command_stop(runner):
    result = runner.invoke(tmn.main, ['stop', mn])
    lines = result.output.splitlines()
    assert lines[0] == 'Stopping masternode {}!'.format(mn)
    assert result.exit_code == 0


def test_command_stop_no_arg(runner):
    result = runner.invoke(tmn.main, ['stop'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2


def test_command_status(runner):
    result = runner.invoke(tmn.main, ['status', mn])
    lines = result.output.splitlines()
    assert lines[0] == 'Masternode {} status:'.format(mn)
    assert result.exit_code == 0


def test_command_status_no_arg(runner):
    result = runner.invoke(tmn.main, ['status'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2
