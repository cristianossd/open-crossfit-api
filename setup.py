from setuptools import setup

setup(
    name='opencrossfitapi',
    packages=['opencrossfitapi'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
    tests_require=[
        'pytest',
    ],
)
