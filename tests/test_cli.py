import pytest
import tmn as package


@pytest.fixture
def runner():
    from click.testing import CliRunner
    runner = CliRunner()
    return runner


def test_ok(*args, **kwargs):
    print('ok')
    print(*args)
    print(**kwargs)
    return True


@pytest.fixture
def tmn():
    from tmn import tmn
    tmn.configuration.networks.devnet = {
        'METRICS_ENDPOINT': 'https://test.com',
        'BOOTNODES': (
            'enode://a601958testc469f17ed30fd0633386a1f1aa95f1630fb81d6ee7'
            '7bf69a84a31bbc0daaa199c00b9ab2d9833cdd994a9107a78661e852ad82f'
            '53a87d8177121f@127.0.0.1:30304'
        ),
        'NETSTATS_HOST': 'test.com',
        'NETSTATS_PORT': '443',
        'WS_SECRET': (
            'test'
        )
    }
    tmn.configuration.networks.testnet = tmn.configuration.networks.devnet
    tmn.configuration.resources.init('tomochain', 'tomo_tests')
    return tmn


def test_version(runner, tmn):
    version = '0.0.5'
    result = runner.invoke(tmn.main, ['--version'])
    assert result.output[-6:-1] == version
    assert package.__version__ == version
    tmn.configuration.resources.user.delete('name')


def test_error_docker(runner, tmn):
    result = runner.invoke(tmn.main, ['--dockerurl', 'unix://test', 'docs'])
    assert '! error: could not access the docker daemon\nNone\n'
    assert result.exit_code != 0
    tmn.configuration.resources.user.delete('name')


def test_command(runner, tmn):
    result = runner.invoke(tmn.main)
    assert result.exit_code == 0
    tmn.configuration.resources.user.delete('name')


def test_command_docs(runner, tmn):
    result = runner.invoke(tmn.main, ['docs'])
    msg = 'Documentation on running a masternode:'
    link = 'https://docs.tomochain.com/\n'
    assert result.output == "{} {}".format(msg, link)
    assert result.exit_code == 0
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_devnet(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    lines = result.output.splitlines()
    assert 'Starting your' in lines[0]
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_testnet(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net',
        'testnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    lines = result.output.splitlines()
    assert 'Starting your' in lines[0]
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_invalid_name(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'tes', '--net', 'devnet'])
    lines = result.output.splitlines()
    assert 'error' in lines[1]
    assert 'name is not valid' in lines[1]
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_no_pkey(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net', 'devnet'])
    lines = result.output.splitlines()
    assert 'error' in lines[1]
    assert 'pkey is required' in lines[1]
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_invalid_pkey_len(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net', 'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890'])
    lines = result.output.splitlines()
    assert 'error' in lines[1]
    assert 'pkey is not valid' in lines[1]
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_invalid_pkey_hex(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net', 'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890zzz'])
    lines = result.output.splitlines()
    assert 'error' in lines[1]
    assert 'pkey is not valid' in lines[1]
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_no_net(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'])
    lines = result.output.splitlines()
    assert 'error' in lines[1]
    assert 'net is required' in lines[1]
    tmn.configuration.resources.user.delete('name')


def test_command_start_init_no_name(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'])
    lines = result.output.splitlines()
    assert 'error' in lines[1]
    assert 'manage any masternode yet' in lines[1]
    tmn.configuration.resources.user.delete('name')


def test_command_start(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['start'])
    lines = result.output.splitlines()
    assert 'Starting' in lines[0]
    tmn.configuration.resources.user.delete('name')


def test_command_start_ignore(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['start', '--name', 'test'])
    lines = result.output.splitlines()
    assert 'warning' in lines[1]
    tmn.configuration.resources.user.delete('name')


def test_command_stop(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['stop'])
    lines = result.output.splitlines()
    assert lines[0] == 'Stopping your masternode!'
    assert result.exit_code == 0
    tmn.configuration.resources.user.delete('name')


def test_command_status(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['status'])
    lines = result.output.splitlines()
    assert lines[0] == 'Your masternode status:'
    assert result.exit_code == 0
    tmn.configuration.resources.user.delete('name')
