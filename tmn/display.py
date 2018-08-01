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
    Return a pastel formated string for browser links

    :param msg: message
    :param url: website url
    :type msg: string
    :type url: string
    """
    return '<highlight_g>{msg}</highlight_g> <link>{url}</link>'.format(
        msg=msg,
        url=url
    )


@style
def warning(msg):
    """
    Return a pastel formated string for warnings

    :param msg: warning message
    :type msg: string
    """
    return '<warning>! warning:</warning> {msg}\n'.format(
        msg=msg
    )


@style
def error(msg):
    """
    Return a pastel formated string for errors

    :param msg: error message
    :type msg: string
    """
    return '<error>! error:</error> {msg}\n'.format(
        msg=msg
    )
