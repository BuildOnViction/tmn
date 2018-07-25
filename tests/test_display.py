from tmn import display


def test_link(capsys):
    display.link('message', 'https://link.com')
    out, err = capsys.readouterr()
    assert out == 'message https://link.com\n'


def test_error(capsys):
    display.error('message')
    out, err = capsys.readouterr()
    assert out == '! error: message\n\n'


def test_warning(capsys):
    display.warning('message')
    out, err = capsys.readouterr()
    assert out == '! warn: message\n\n'
