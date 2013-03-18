# pywhich #

Find Python modules on the current python path with `pywhich`.

## Usage ##

    $ pywhich termtool
    Module 'termtool' not found (ImportError: No module named termtool)
    $ pip install termtool
    ...
    Successfully installed termtool
    Cleaning up...
    $ pywhich termtool
    /Users/markpasc/Work/pywhich/.env/lib/python2.7/site-packages/termtool.py
    $ pywhich --ver termtool
    1.0
    $

## Install ##

Install `pywhich` as any other Python program, with:

    $ python setup.py install

`pywhich` will then be available to use in the Python environment you installed it in.
