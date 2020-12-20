from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "0.1"

setup(
    name='file_format_converter',
    version=VERSION,
    license='Apache Software License (Apache Software License 2.0)',
    author='Agit Oktay',
    author_email='agitoktay@gmail.com',
    description='A command line tool that validate and trasnform data from csv to desired file format like JSON and XML',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.5",
    packages=find_packages(exclude=['tests*']),
    url='https://github.com/agtokty/csv2others',
    download_url='https://github.com/agtokty/csv2others/archive/%s.tar.gz' % VERSION,
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': [
            'ffc = csv2others.app:main'
        ]}
)
