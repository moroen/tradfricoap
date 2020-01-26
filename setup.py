from setuptools import setup

setup(
    name="tradfricoap",
    version="0.0.4",
    url="https://github.com/moroen/tradfricoap.git",
    author="moroen",
    author_email="moroen@gmail.com",
    description="Controlling IKEA-Tradfri from the commmand line",
    packages=["tradfricoap"],
    include_package_data=True,
    setup_requires=["cython"],
    install_requires=["cython"],
    scripts=["tradfri"],
)
