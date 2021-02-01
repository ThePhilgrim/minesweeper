"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['minesweeper.py']
DATA_FILES = ['doomguy.gif', 'bomb_small.png', 'bomb.png', 'button_small.png', 'flag_small.png', 'pressed_button_small.png']
OPTIONS = {}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
