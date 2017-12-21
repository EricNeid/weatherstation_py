"""
setup for module
"""
import setuptools


def get_readme():
    """return content of README"""
    with open("README.md") as f:
        return f.read()


def get_license():
    """return licence"""
    with open('LICENSE') as f:
        return f.read()


setuptools.setup(
    name='weatherstation',
    version='1.0.0',
    description='Simple Weatherstation for raspberry pi using OpenWeatherMaps API',
    long_description=get_readme(),
    author='Eric Neidhardt',
    author_email='eric.neidhardt@gmail.com',
    url='',
    license=get_license(),
    packages=setuptools.find_packages(exclude=('tests', 'docs'))
)
