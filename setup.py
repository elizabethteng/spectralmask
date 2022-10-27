from setuptools import setup, find_packages

# taken from orbitize

def get_requires():
    reqs = []
    for line in open("requirements.txt","r").readlines():
        reqs.append(line)
    return reqs

setup(
name = "spectralmask",
version = "0.0",
description = "applies masks for analysis of absorption spectra",
url = "https://github.com/elizabethteng/spectralmask",
license = "MIT",
packages = find_packages(),
install_requires = get_requires()
)
