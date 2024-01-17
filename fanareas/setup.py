from setuptools import find_packages, setup

setup(
    name="fanareas",
    packages=find_packages(exclude=["fanareas_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "pandas",
        "dagster-postgres"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
