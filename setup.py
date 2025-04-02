from setuptools import setup, find_packages

setup(
    name="sales-tracker",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'flask',
        'duckdb',
        'redis',
        'werkzeug',
    ],
    python_requires='>=3.7',
) 