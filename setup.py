import sys
from os import (
    path,
)

from setuptools import (
    find_packages,
    setup,
)

import imugi

if sys.version_info < (3, 6):
    sys.exit('imugi only supports Python 3.6 or later')

VERSION = imugi.__version__
DOWNLOAD_URL = f'https://github.com/hahnlee/imugi/archive/{VERSION}.tar.gz'

project_dir: str = path.abspath(path.join(path.dirname(__file__)))

with open(path.join(project_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='imugi',
    version=VERSION,
    description='The experimental python compiler written in python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Han Lee',
    author_email='hanlee.dev@gmail.com',
    url='https://github.com/hahnlee/imugi',
    install_requires=[
        'llvmlite>=0.23.0',
    ],
    extras_require={
        'dev': [
            'flake8',
            'isort',
        ],
    },
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'imugi=imugi.compiler.main:main',
        ],
    },
    keywords=[
        'compiler',
        'compiler-frontend',
        'imugi',
        'llvm',
        'parser',
        'programming language',
        'python',
    ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Build Tools',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
    ],
    download_url=DOWNLOAD_URL,
)
