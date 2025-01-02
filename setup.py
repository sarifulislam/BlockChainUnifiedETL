from setuptools import setup, find_packages

try:
    with open("README.md", "r") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A Python package for blockchain ETL operations."

setup(
    name="blockchainETL",
    version="0.1.0",
    description="A Python package for blockchain ETL operations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sk Sariful Islam",
    author_email="sarifulislam680@gmail.com",
    url="https://github.com/sarifulislam/blockchainETL.git",
    packages=find_packages(),
    install_requires=[
        "requests",
        "web3",
        "sqlalchemy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
