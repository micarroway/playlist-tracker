#!/usr/bin/env python

from distutils.core import setup

setup(
    name='PlaylistTracker',
    version='1.0',
    description='Statistics for a shared Spotify playlist',
    author='Jaimie Catoe',
    author_email='',
    url='https://github.com/jcatoe/playlist-tracker',
    packages=['PlaylistTracker'],
    data_files=[
        ('config', ['app_config.json'])
    ]
)
