
from setuptools import find_packages, setup


setup(
    name='rinex',
    version='0.1.0',
    description='RINEX file name checker',
    url='',
    author='Joachim Mortensen <joachim.mortensen@protonmail.com>',
    license='',
    zip_safe=False,

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    package_data={
        'rinex': [
            'ISO_3166-1_alpha-3.dat',
        ],
    },
    include_package_data=True,

    install_requires=[
    ],

    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
)
