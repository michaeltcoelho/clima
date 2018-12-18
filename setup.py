from setuptools import setup, find_packages

requirements = [
    'beautifulsoup4==4.6.3',
    'beautifultable==0.5.3',
    'Click==7.0',
    'huepy==0.9.8.1',
    'selenium==3.141.0',
]

testing_requirements = [
    'pytest==4.0.2',
]

setup(
    name='clima',
    version='0.1.0',
    description='Climatempo crawler',
    author='michaeltcoelho',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'testing': testing_requirements,
    },
    entry_points={
        'console_scripts': [
            'clima = clima.cli:clima',
        ]
    }
)
