# -*- encoding: utf8 -*-
import os, io, sys
from glob import glob
from setuptools import setup, find_packages

def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()

data_files = [
    ('/opt/simmetrica/config', ['config/config.yml']),
    ('/opt/simmetrica/static/javascripts', glob('static/javascripts/*')),
    ('/opt/simmetrica/static/stylesheets', glob('static/stylesheets/*')),
    ('/opt/simmetrica/templates', glob('templates/*')),
]

setup(
    name="simmetrica",
    version="1.0.2",
    url='https://github.com/o/simmetrica',
    license='MIT',
    description='Library for collecting, aggregating and visualizing event '
                'metrics as timeseries data',
    long_description=read('README.md'),
    author='Osman Üngür',
    author_email='osmanungur@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: System :: Monitoring'
    ],
    keywords=[
        'event', 'metric', 'timeseries', 'statistics',
    ],
    install_requires=['redis','flask','pyyaml'],
    tests_require=['mock'],
    scripts=glob('bin/*'),
    data_files=data_files
)

