from setuptools import find_packages, setup

setup(
    name='flasknet',
    version='0.1.0',
    description='A simple social network made with Flask.',
    author='Tobias Vossen',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'start = flasknet:main',
        ],
    },
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8'
    ]
)
