from setuptools import setup, find_packages

setup(
    name="tool314",
    version="0.1.0",
    description="A lightweight utility for Raspberry Pi system management (Fan, OC, DNS).",
    author="Doğukan Sahil",
    author_email="hi@dogukansahil.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "tool314=tool314.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
)
