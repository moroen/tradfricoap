from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tradfricoap",
    version="0.0.11",
    url="https://github.com/moroen/tradfricoap.git",
    author="moroen",
    author_email="moroen@gmail.com",
    description="Controlling IKEA-Tradfri",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=["tradfricoap"],
    include_package_data=True,
    setup_requires=[],
    install_requires=["py3coap", "appdirs"],
    scripts=["tradfri"],
)
