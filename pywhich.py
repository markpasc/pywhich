import logging
from optparse import OptionParser
import os
import sys


log = logging.getLogger('pywhich')
"""A logger in the ``pywhich`` scope."""


class ModuleNotFound(Exception):
    """The requested module could not be imported."""
    pass


def identify_module(arg):
    """Import and return the Python module named in `arg`.

    If the module cannot be imported, a `pywhich.ModuleNotFound` exception is
    raised.

    """
    try:
        __import__(arg)
    except Exception:
        exc = sys.exc_info()[1]
        raise ModuleNotFound("%s: %s" % (type(exc).__name__, str(exc)))

    mod = sys.modules[arg]
    return mod


def identify_filepath(arg, real_path=None, show_directory=None,
    find_source=None, hide_init=None):
    """Discover and return the disk file path of the Python module named in
    `arg` by importing the module and returning its ``__file__`` attribute.

    If `find_source` is `True`, the named module is a ``pyc`` or ``pyo`` file,
    and a corresponding ``.py`` file exists on disk, the path to the ``.py``
    file is returned instead.

    If `show_directory` is `True`, the path to the directory containing the
    discovered module file is returned. Similarly, if `hide_init` is `True` and
    the named module is the ``__init__`` module of a package, the function
    returns the path to the package directory containing the ``__init__.py``
    filename.

    If `real_path` is `True` and the discovered module was loaded via symlink,
    the real path (as determined by `os.path.realpath()`) is returned.

    If the named module cannot be imported or its path on disk determined, this
    function raises a `pywhich.ModuleNotFound` exception.

    """
    mod = identify_module(arg)  # raises ModuleNotFound
    try:
        filename = mod.__file__
    except AttributeError:
        raise ModuleNotFound("module has no '__file__' attribute; is it a "
            "built-in or C module?")

    if find_source and (filename.endswith('.pyc') or filename.endswith('.pyo')):
        log.debug("Filename ends in pyc or pyo, so looking for the .py file")
        sourcefile = filename[:-1]
        if os.access(sourcefile, os.F_OK):
            filename = sourcefile
        else:
            log.debug("Did not find .py file for path %r, using as-is",
                filename)

    if real_path:
        filename = os.path.realpath(filename)

    if show_directory or (hide_init and
        os.path.basename(filename).startswith('__init__.')):
        log.debug("Showing directories or hiding __init__s, so returning "
            "directory of %r", filename)
        filename = os.path.dirname(filename)

    return filename


def identify_modules(*args, **kwargs):
    """Find the disk locations of the given named modules, printing the
    discovered paths to stdout and errors discovering paths to stderr.

    Any provided keyword arguments are passed to `identify_filepath()`.

    """
    if len(args) == 1:
        path_template = "%(file)s"
        error_template = "Module '%(mod)s' not found (%(error)s)"
    else:
        path_template = "%(mod)s: %(file)s"
        error_template = "%(mod)s: not found (%(error)s)"

    for modulename in args:
        try:
            filepath = identify_filepath(modulename, **kwargs)
        except ModuleNotFound:
            exc = sys.exc_info()[1]
            sys.stderr.write(error_template % {
                'mod': modulename,
                'error': str(exc),
            })
            sys.stderr.write('\n')
        else:
            print(path_template % {
                'mod': modulename,
                'file': filepath
            })


def find_version(*args):
    """Find the versions of the given named modules, printing the discovered
    versions to stdout and errors discovering versions to stderr."""
    if len(args) == 1:
        ver_template = "%(version)s"
        error_template = "Distribution/module '%(mod)s' not found (%(error)s)"
    else:
        ver_template = "%(mod)s: %(version)s"
        error_template = "%(mod)s: not found (%(error)s)"

    import pkg_resources
    for modulename in args:
        try:

            try:
                dist = pkg_resources.get_distribution(modulename)
            except pkg_resources.DistributionNotFound:

                mod = identify_module(modulename)  # raises ModuleNotFound
                if not hasattr(mod, '__version__'):
                    raise ModuleNotFound('module has no __version__')
                version = mod.__version__

            else:
                version = dist.version

        except ModuleNotFound:
            exc = sys.exc_info()[1]
            sys.stderr.write(error_template % {
                'mod': modulename,
                'error': str(exc),
            })
            sys.stderr.write('\n')
        else:
            print(ver_template % {
                'mod': modulename,
                'version': version,
            })


def main(argv=None):
    """Run the pywhich command as if invoked with arguments `argv`.

    If `argv` is `None`, arguments from `sys.argv` are used.

    """
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
    parser.add_option('--ver', action="store_true", dest="find_version",
        default=False, help="find the version of the named package, not the location on disk")

    opts, args = parser.parse_args()

    verbose = max(0, min(4, opts.verbose))
    log_levels = (logging.CRITICAL, logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG)
    logging.basicConfig()
    log.setLevel(log_levels[verbose])

    if opts.find_version:
        find_version(*args)
    else:
        kwargs = dict((fld, getattr(opts, fld)) for fld
            in ('real_path', 'show_directory', 'find_source', 'hide_init'))
        identify_modules(*args, **kwargs)

    return 0


if __name__ == '__main__':
    sys.exit(main())
