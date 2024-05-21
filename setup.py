from setuptools import setup, find_packages

setup(
    name="tinkoff_acquiring",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "aiohttp",
    ],
    author="Artem",
    author_email="support@sm1ky.com",
    description="A Python client for Tinkoff Acquiring API",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sm1ky/tinkoff_acquiring",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)
