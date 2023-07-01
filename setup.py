""" Setup file """

from setuptools import setup

from sama import __app_name__, __version__

setup(
    name=__app_name__,
    version=__version__,
    author="Luis Ch.",
    description="Simple inventory and sales manager.",
    entry_points={
        "console_scripts": [
            f"{__app_name__} = {__app_name__}.__main__:main",
        ]
    },
)
