import pytest

import docker

import tmn as package

client = docker.from_env()


@pytest.fixture
def runner():
    from click.testing import CliRunner
    runner = CliRunner()
    return runner


@pytest.fixture
def tmn():
    from tmn import tmn
    from tmn.environments import environments
    from tmn import configuration
    environments['devnet'] = {
        'tomochain': {
            'BOOTNODES': (
                'test'
            ),
            'NETSTATS_HOST': 'test.com',
            'NETSTATS_PORT': '443',
            'NETWORK_ID': '90',
            'WS_SECRET': (
                'test'
            )
        },
        'metrics': {
            'METRICS_ENDPOINT': 'https://test.com'
        }
    }
    environments['testnet'] = environments['devnet']
    configuration.resources.init('tomochain', 'tomo_tests')
    return tmn


def _clean(tmn):
    from tmn import configuration
    try:
        client.containers.get('test1_tomochain').remove(force=True)
    except Exception:
        pass
    try:
        client.containers.get('test1_metrics').remove(force=True)
    except Exception:
        pass
    try:
        client.volumes.get('test1_chaindata').remove(force=True)
    except Exception:
        pass
    try:
        client.networks.get('test1_tmn').remove()
    except Exception:
        pass
    configuration.resources.init('tomochain', 'tomo_tests')
    configuration.resources.user.delete('id')
    configuration.resources.user.delete('name')
    configuration.resources.user.delete('net')


def test_version(runner, tmn):
    version = '0.5.1'
    result = runner.invoke(tmn.main, ['--version'])
    assert result.output[-6:-1] == version
    assert package.__version__ == version


def test_error_docker(runner, tmn):
    result = runner.invoke(tmn.main, ['--docker', 'unix://test', 'docs'])
    assert '! error: could not access the docker daemon\nNone\n'
    assert result.exit_code == 0


def test_command(runner, tmn):
    result = runner.invoke(tmn.main)
    assert result.exit_code == 0


def test_command_docs(runner, tmn):
    result = runner.invoke(tmn.main, ['docs'])
    msg = 'Documentation on running a masternode:'
    link = 'https://docs.tomochain.com/masternode/tmn/\n'
    assert result.output == "{} {}".format(msg, link)
    assert result.exit_code == 0


def test_command_start_init_devnet(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    lines = result.output.splitlines()
    assert 'Starting masternode test1:' in lines
    for line in lines:
        assert '✗' not in line
    _clean(tmn)


def test_command_start_init_testnet(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'testnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    lines = result.output.splitlines()
    assert 'Starting masternode test1:' in lines
    for line in lines:
        assert '✗' not in line
    _clean(tmn)


def test_command_start_init_mainnet(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'mainnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    lines = result.output.splitlines()
    assert 'Starting masternode test1:' in lines
    for line in lines:
        assert '✗' not in line
    _clean(tmn)


def test_command_start_init_invalid_name(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'tes', '--net', 'devnet', '--pkey', '1234'])
    lines = result.output.splitlines()
    assert 'error' in lines[1]
    assert '! error: --name is not valid' in lines
    _clean(tmn)


def test_command_start_init_no_pkey(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net', 'devnet'])
    lines = result.output.splitlines()
    assert ('! error: --pkey is required when starting a new '
            'masternode') in lines
    _clean(tmn)


def test_command_start_init_invalid_pkey_len(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net', 'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890'])
    lines = result.output.splitlines()
    assert '! error: --pkey is not valid' in lines
    _clean(tmn)


def test_command_start_init_no_net(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'])
    lines = result.output.splitlines()
    assert '! error: --net is required when starting a new masternode' in lines
    _clean(tmn)


def test_command_start_init_no_name(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'])
    lines = result.output.splitlines()
    assert ('! error: --name is required when starting a new '
            'masternode') in lines
    _clean(tmn)


def test_command_start(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['start'])
    lines = result.output.splitlines()
    assert 'Starting masternode test1:' in lines
    for line in lines:
        assert '✗' not in line
    _clean(tmn)


def test_command_start_ignore(runner, tmn):
    result = runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['start', '--name', 'test'])
    lines = result.output.splitlines()
    assert '! warning: masternode test1 is already configured' in lines
    _clean(tmn)


def test_command_stop(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['stop'])
    lines = result.output.splitlines()
    assert 'Stopping masternode test1:' in lines
    for line in lines:
        assert '✗' not in line
    _clean(tmn)


def test_command_status(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['status'])
    lines = result.output.splitlines()
    assert 'Masternode test1 status:' in lines
    _clean(tmn)


def test_command_inspect(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['inspect'])
    lines = result.output.splitlines()
    assert 'Masternode test1 details:' in lines
    _clean(tmn)


def test_command_update(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['update'])
    lines = result.output.splitlines()
    assert 'Updating masternode test1:' in lines
    for line in lines:
        assert '✗' not in line
    _clean(tmn)


def test_command_remove(runner, tmn):
    runner.invoke(tmn.main, [
        'start', '--name', 'test1', '--net',
        'devnet', '--pkey',
        '0123456789012345678901234567890123456789012345678901234567890123'
    ])
    result = runner.invoke(tmn.main, ['remove', '--confirm'])
    lines = result.output.splitlines()
    assert 'Removing masternode test1:' in lines
    for line in lines:
        assert '✗' not in line
    _clean(tmn)
