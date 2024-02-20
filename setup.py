# setup.py

from setuptools import setup, find_packages

setup(
    name="syn_data_fidelity",
    description="Assessing fidelity of synthetic data",
    author="Ulli Schaechtle",
    author_email="ulli@mit.edu",
    packages=["syn_data_fidelity"],
    package_dir={"syn_data_fidelity": "src"},
    install_requires=[
        # XXX:List any package dependencies here
        # e.g., 'numpy>=1.18.1',
    ],
)
