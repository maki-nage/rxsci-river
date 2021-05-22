import sys

try:
    from setuptools import setup, find_packages
    use_setuptools = True
except ImportError:
    from distutils.core import setup
    use_setuptools = False

try:
    with open('README.rst', 'rt') as readme:
        description = '\n' + readme.read()
except IOError:
    # maybe running setup.py from some other dir
    description = ''

python_requires = '>=3.6'
install_requires = [
    'river>=0.7',
    'rxsci>=0.7',
    'scikit-learn>=0.24',
]

setup(
    name="rxsci-river",
    version='0.1.0',
    url='https://github.com/maki-nage/rxsci-river.git',
    license='MIT',
    description="River-Ml integration into RxSci",
    long_description=description,
    author='Romain Picard',
    author_email='romain.picard@oakbits.com',
    packages=find_packages(),
    install_requires=install_requires,
    platforms='any',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    project_urls={
        'Documentation': 'https://www.makinage.org/doc/rxsci-river/latest/index.html',
    }
)
