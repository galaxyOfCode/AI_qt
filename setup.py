from setuptools import setup

APP = ['ai.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['os', 'sys', 'PyQt6', 'openai', 'pyperclip'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)