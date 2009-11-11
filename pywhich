#!/usr/bin/env python

import logging
from optparse import OptionParser
import os
import sys

DOT = '.'

log = logging.getLogger('pywhich')


class ModuleNotFound(Exception):
    pass


def identify_module(arg, real_path=None, show_directory=None,
    find_source=None, hide_init=None):
    try:
        __import__(arg)
    except Exception, exc:
        raise ModuleNotFound("%s: %s" % (type(exc).__name__, str(exc)))

    mod = sys.modules[arg]
    filename = mod.__file__

    if find_source and (filename.endswith('.pyc') or filename.endswith('.pyo')):
        sourcefile = filename[:-1]
        if os.access(sourcefile, os.F_OK):
            filename = sourcefile

    if real_path:
        filename = os.path.realpath(filename)

    if show_directory or (hide_init and
        os.path.basename(filename).startswith('__init__.')):
        filename = os.path.dirname(filename)

    return filename


def identify_modules(*args, **kwargs):
    if len(args) == 1:
        path_template = "%(file)s"
        error_template = "Module '%(mod)s' not found (%(error)s)"
    else:
        path_template = "%(mod)s: %(file)s"
        error_template = "%(mod)s: not found (%(error)s)"

    for modulename in args:
        try:
            filepath = identify_module(modulename, **kwargs)
        except ModuleNotFound, exc:
            print >>sys.stderr, error_template % {
                'mod': modulename,
                'error': str(exc),
            }
        else:
            print path_template % {
                'mod': modulename,
                'file': filepath
            }


def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = OptionParser()

    parser.add_option('-v', '--verbose', dest="verbose", action="count",
        default=2, help="be chattier (stackable)")
    def quiet(option, opt_str, value, parser):
        parser.values.verbose -= 1
    parser.add_option('-q', '--quiet', action="callback", callback=quiet,
        help="be less chatty (stackable)")

    parser.add_option('-r', action="store_true", dest="real_path",
        default=False, help="dereference symlinks")
    parser.add_option('-b', action="store_true", dest="show_directory",
        default=False, help="show directory instead of filename")
    parser.add_option('-i', '--hide-init', action="store_true", dest="hide_init",
        default=False, help="show directory if the module ends in __init__.py")
    parser.add_option('-s', '--source', action="store_true", dest="find_source",
        default=False, help="find .py files for .pyc/.pyo files")

    opts, args = parser.parse_args()

    log_levels = (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
    logging.basicConfig()
    log.setLevel(log_levels[opts.verbose % 5])

    kwargs = dict((fld, getattr(opts, fld)) for fld
        in ('real_path', 'show_directory', 'find_source', 'hide_init'))
    identify_modules(*args, **kwargs)

    return 0


if __name__ == '__main__':
    sys.exit(main())

