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
    ('share/doc', ['README.md', 'config/config.yml']),
    ('simmetrica/static/javascripts', glob('static/javascripts/*')),
    ('simmetrica/static/stylesheets', glob('static/stylesheets/*')),
    ('simmetrica/templates', glob('templates/*')),
]

if hasattr(sys, 'real_prefix') or 'bsd' in sys.platform:
    conf_path = os.path.join(sys.prefix, 'etc', 'simmetrica')
elif not hasattr(sys, 'real_prefix') and 'linux' in sys.platform:
    conf_path = os.path.join('/etc', 'simmetrica')
elif 'darwin' in sys.platform:
    conf_path = os.path.join('/usr/local', 'etc', 'simmetrica')
elif 'win32' in sys.platform:
    conf_path = os.path.join(os.environ.get('APPDATA'), 'simmetrica')
data_files.append((conf_path, ['config/config.yml']))

setup(
    name="simmetrica",
    version="1.0",
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

