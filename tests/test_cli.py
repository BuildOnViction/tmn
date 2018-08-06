import pytest
import tmn as package
from tmn import tmn


@pytest.fixture
def runner():
    from click.testing import CliRunner
    runner = CliRunner()
    return runner


def test_version(runner):
    version = '0.0.2'
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


def test_command_opt_config(runner):
    result = runner.invoke(tmn.main, ['--config', '/tmp/tmn', 'docs'])
    assert 'Documentation' in result.output
    assert result.exit_code == 0


def test_command_opt_config_fail_directory(runner):
    result = runner.invoke(tmn.main, ['--config', '/root', 'docs'])
    assert '! error' in result.output
    assert result.exit_code != 0


def test_command_opt_config_fail_access(runner):
    result = runner.invoke(tmn.main, ['--config', '/root/tmn', 'docs'])
    assert '! error' in result.output
    assert result.exit_code != 0


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


def test_command_start(runner):
    result = runner.invoke(tmn.main, ['start'])
    lines = result.output.splitlines()
    assert lines[0] == 'Starting your masternode!'
    assert lines[2] == 'Volumes'
    assert lines[4][:32] == '  - Creating blockchain_data... '
    assert lines[4][32:] in ['exists', 'created']
    assert lines[6] == 'Networks'
    assert lines[8][:27] == '  - Creating masternode... '
    assert lines[8][27:] in ['exists', 'created']
    assert lines[10] == 'Containers'
    assert lines[12][:24] == '  - Creating metrics... '
    assert lines[12][24:] in ['exists', 'created']
    assert lines[13][:26] == '  - Creating tomochain... '
    assert lines[13][26:] in ['exists', 'created']
    assert lines[15][:24] == '  - Starting metrics... '
    assert lines[15][24:] in [
        'restarting', 'running'
    ]
    assert lines[16][:26] == '  - Starting tomochain... '
    assert lines[16][26:] in [
        'restarting', 'running'
    ]
    assert result.exit_code == 0


def test_command_stop(runner):
    result = runner.invoke(tmn.main, ['stop'])
    lines = result.output.splitlines()
    assert lines[0] == 'Stopping your masternode!'
    assert result.exit_code == 0
