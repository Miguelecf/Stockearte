from setuptools import setup

setup(
    name='server',
    version='0.1',
    install_requires=[
        'grpcio',
        'grpcio-tools',
    ],
    packages=['src'],
)