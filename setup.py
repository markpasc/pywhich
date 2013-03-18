from distutils.core import setup

setup(
    name='pywhich',
    version='1.1',
    description='Find where Python modules are installed in the current Python',
    scripts=['bin/pywhich'],
    author='Mark Paschal',
    author_email='markpasc@markpasc.org',
    url='https://github.com/markpasc/pywhich',
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
