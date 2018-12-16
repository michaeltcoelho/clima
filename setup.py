from setuptools import setup, find_packages

requirements = [
    'beautifulsoup4==4.6.3',
    'selenium==3.141.0',
    'Click==7.0',
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
    install_requires=requirements,
    extras_require={
        'testing': testing_requirements,
    },
    entry_points={
        'console_scripts': [
            'clima = crawler.cli:clima',
        ]
    }
)
