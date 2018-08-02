from click.testing import CliRunner
import tmn as package
from tmn import tmn

runner = CliRunner()


def test_version():
    version = '0.0.1'
    result = runner.invoke(tmn.main, ['--version'])
    assert result.output[-6:-1] == version
    assert package.__version__ == version


def test_error_docker():
    result = runner.invoke(tmn.main, ['--dockerurl', 'unix://fail', 'docs'])
    assert result.output == '! error: could not access the docker deamon\n\n'
    assert result.exit_code != 0


def test_command():
    result = runner.invoke(tmn.main)
    assert result.exit_code == 0


def test_command_opt_config():
    result = runner.invoke(tmn.main, ['--config', '/tmp/tmn', 'docs'])
    assert 'Documentation' in result.output
    assert result.exit_code == 0


def test_command_opt_config_fail_directory():
    result = runner.invoke(tmn.main, ['--config', '/root', 'docs'])
    assert '! error' in result.output
    assert result.exit_code != 0


def test_command_opt_config_fail_access():
    result = runner.invoke(tmn.main, ['--config', '/root/tmn', 'docs'])
    assert '! error' in result.output
    assert result.exit_code != 0


def test_command_docs():
    result = runner.invoke(tmn.main, ['docs'])
    msg = 'Documentation on running a masternode:'
    link = 'https://docs.tomochain.com/\n'
    assert result.output == "{} {}".format(msg, link)
    assert result.exit_code == 0


def test_command_docs_opt_open():
    result = runner.invoke(tmn.main, ['docs', '--open'])
    msg = 'Opening documentation:'
    link = 'https://docs.tomochain.com/\n'
    assert result.output == "{} {}".format(msg, link)
    assert result.exit_code == 0


def test_command_start():
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
    assert lines[12][:25] == '  - Creating telegraf... '
    assert lines[12][25:] in ['exists', 'created']
    assert lines[13][:26] == '  - Creating tomochain... '
    assert lines[13][26:] in ['exists', 'created']
    assert lines[15][:25] == '  - Starting telegraf... '
    assert lines[15][25:] in [
        'restarting', 'running'
    ]
    assert lines[16][:26] == '  - Starting tomochain... '
    assert lines[16][26:] in [
        'restarting', 'running'
    ]
    assert result.exit_code == 0
