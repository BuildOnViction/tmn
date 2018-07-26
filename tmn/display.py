import pastel

pastel.add_style('highlight_g', 'green')
pastel.add_style('highlight_y', 'yellow')
pastel.add_style('link', 'yellow', options=['underscore'])
pastel.add_style('warning', 'yellow')
pastel.add_style('error', 'red')


def style(function):
    """
    Print and colorize strings with `pastel`

    :param function: the string returning function
    :type function: function
    """
    def wrapper(*args):
        print(pastel.colorize(function(*args)))
    return wrapper


@style
def link(msg, url):
    """
    Display a line formated for browser links

    :param msg: message
    :param url: website url
    :type msg: string
    :type url: string
    """
    return f'<highlight_g>{msg}</highlight_g> <link>{url}</link>'


@style
def warning(msg):
    """
    Display a line formated for warnings

    :param msg: warning message
    :type msg: string
    """
    return f'<warning>! warning: {msg}</warning>\n'


@style
def error(msg):
    """
    Display a line formated for errors

    :param msg: error message
    :type msg: string
    """
    return f'<error>! error: {msg}</error>\n'
