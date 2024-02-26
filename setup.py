from setuptools import setup

setup(
    name="syn_data_fidelity",
    description="Assessing fidelity of synthetic data",
    author="Ulli Schaechtle",
    author_email="ulli@mit.edu",
    packages=["syn_data_fidelity", "fidelity_cli"],
    package_dir={"syn_data_fidelity": "src", "fidelity_cli": "bin"},
    install_requires=[
        # XXX:This is solved via flake.nix.
        # Not filling anything in here to avoid duplication.
    ],
    entry_points={
        "console_scripts": [
            "assess-distance=fidelity_cli.dist:main",
            "assess-statistics=fidelity_cli.two_sample_testing:main",
        ],
    },
)
