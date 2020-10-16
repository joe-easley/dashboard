from setuptools import setup, find_packages
import pyinstaller


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
        name="ukcovid19tool",
        version="1.0",
        description="Calls gov API and displays requested charts",
        author="Joe Easley",
        url="https://github.com/joe-easley/dashboard",
        packages=find_packages(),
        long_description=long_description,
        include_package_data=True
)
