"""
Setup for xapi-db-load.
"""
from setuptools import find_packages, setup

from aspects import __version__

with open("README.rst", "r") as readme:
    desc = readme.read()

setup(
    name="openedx-aspects",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    entry_points="""
        [console_scripts]
        xapi-db-load=aspects.xapi_db_load.main:cli
    """,
    install_requires=[
        "click",
        "clickhouse-connect >= 0.5, < 0.7",
        "requests",
        "smart_open[s3]",
    ],
    url="https://github.com/openedx/openedx-aspects",
    project_urls={
        "Code": "https://github.com/openedx/openedx-aspects",
        "Issue tracker": "https://github.com/openedx/openedx-aspects/issues",
    },
    license="Apache 2",
    author="Open edX",
    description="Code for the Open edX Aspects data project.",
    long_description=desc,
    long_description_content_type="text/x-rst",
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache 2",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
