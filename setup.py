from distutils.core import setup

setup(
    name='pywhich',
    version='1.1',
    description='Find where Python modules are installed in the current Python',
    py_modules=['pywhich'],
    scripts=['bin/pywhich'],
)
