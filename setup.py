from setuptools import setup, find_packages

install_requires = [
    "redis==5.0.1",
    "typing_extensions==4.8.0",
    "pydantic==2.4.2",
    "pydantic_core==2.10.1",
    "elasticsearch==8.10.0",
    "flask==3.0.0",
    "flask-socketio==5.3.6"
]

setup(
    name='noauth',
    version='0.1.0',
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=install_requires,
    tests_require=[
        'pytest',
    ],
)