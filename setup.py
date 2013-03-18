from setuptools import setup

setup(
    name='simmetrica',
    py_modules=['simmetrica'],
    version='0.0.1',
    description='Library for collecting, aggregating and visualizing event '
                'metrics as timeseries data',
    author='Osman Ungur',
    author_email='osmanungur@gmail.com',
    url='https://github.com/import/simmetrica'
    install_requires=[
        'redis'
    ],
    tests_require=['mock'],
)
