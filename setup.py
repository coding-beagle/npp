from setuptools import setup, find_packages

setup(
    name='nanoplusplus',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'npp = nanoplusplus.scripts.nanoplusplus:cli',
        ],
    },
)
