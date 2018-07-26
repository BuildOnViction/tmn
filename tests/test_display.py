from tmn import display


def test_decorator(capsys):
    @display.style
    def return_string(msg):
        return f'{msg}'
    return_string('test')
    out, err = capsys.readouterr()
    assert out == 'test\n'


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
    assert out == '! warning: message\n\n'
