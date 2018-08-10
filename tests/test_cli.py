import pytest
import tmn as package
from tmn import tmn

mn_name = 'test'
# le = len(mn_name)


@pytest.fixture
def runner():
    from click.testing import CliRunner
    runner = CliRunner()
    return runner


def test_version(runner):
    version = '0.0.3'
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


def test_command_start(runner):
    result = runner.invoke(tmn.main, ['start', mn_name])
    lines = result.output.splitlines()
    assert lines[0] == 'Starting masternode {}!'.format(mn_name)
    assert result.exit_code == 0
    n = tmn.masternode._client.networks.get('{}_network'.format(mn_name))
    c = tmn.masternode._client.volumes.get('{}_data'.format(mn_name))
    for container in tmn.masternode._get_containers(name=mn_name):
        container.remove(force=True)
    c.remove(force=True)
    n.remove()


def test_command_start_no_arg(runner):
    result = runner.invoke(tmn.main, ['start'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2


def test_command_stop(runner):
    result = runner.invoke(tmn.main, ['stop', mn_name])
    lines = result.output.splitlines()
    assert lines[0] == 'Stopping masternode {}!'.format(mn_name)
    assert result.exit_code == 0


def test_command_stop_no_arg(runner):
    result = runner.invoke(tmn.main, ['stop'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2


def test_command_status(runner):
    result = runner.invoke(tmn.main, ['status', mn_name])
    lines = result.output.splitlines()
    assert lines[0] == 'Masternode {} status:'.format(mn_name)
    assert result.exit_code == 0


def test_command_status_no_arg(runner):
    result = runner.invoke(tmn.main, ['status'])
    lines = result.output.splitlines()
    assert 'Usage' in lines[0]
    assert result.exit_code == 2
