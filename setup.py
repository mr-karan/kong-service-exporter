#!/usr/bin/env python
from codecs import open
from setuptools import setup

README = open("README.md").read()

def requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()



setup(
    name="kong-service-exporter",
    version="0.1.1",
    description="A small utility to export a Markdown file containing the list of services and other useful information from Kong's config.",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Karan Sharma",
    author_email="hello@mrkaran.dev",
    url="https://github.com/mr-karan/kong-service-exporter",
    packages=['kong_service_exporter'],
    install_requires=requirements(),
    include_package_data=True,
    download_url="https://github.com/mr-karan/kong-service-exporter",
    license="MIT License",
    entry_points={
        'console_scripts': [
            'kong-service-exporter = kong_service_exporter.generate:main'
        ],
    },
    classifiers=[
        "Topic :: Documentation"
    ],
)