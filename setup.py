from setuptools import setup, find_packages


setup(
    name='libcheckers',
    version='0.1.1',
    description='International checkers gameplay library for the CS301 AI course at UCU',
    url='https://github.com/YuriyGuts/libcheckers',
    author='Yuriy Guts',
    author_email='yuriy.guts@gmail.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
