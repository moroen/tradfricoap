from setuptools import setup

setup(
    name="tradfricoap",
    version="0.0.5",
    url="https://github.com/moroen/tradfricoap.git",
    author="moroen",
    author_email="moroen@gmail.com",
    description="Controlling IKEA-Tradfri",
    packages=["tradfricoap"],
    include_package_data=True,
    setup_requires=[],
    install_requires=["py3coap", "appdirs"],
    scripts=["tradfri"],
)
