from click.testing import CliRunner
import tmn as package
from tmn import tmn

runner = CliRunner()


def test_version():
    version = '0.0.1'
    result = runner.invoke(tmn.main, ['--version'])
    assert result.output[-6:-1] == version
    assert package.__version__ == version


def test_command():
    result = runner.invoke(tmn.main)
    assert result.exit_code == 0


def test_command_docs():
    result = runner.invoke(tmn.main, ['docs'])
    msg = 'You can find documentation on running a masternode here:'
    link = 'https://docs.tomochain.com/\n'
    assert result.output == "{} {}".format(msg, link)


def test_command_docs_open():
    result = runner.invoke(tmn.main, ['docs', '--open'])
    msg = 'Opening documentation:'
    link = 'https://docs.tomochain.com/\n'
    assert result.output == "{} {}".format(msg, link)
