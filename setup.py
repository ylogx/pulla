from distutils.core import setup

def get_version():
    import pulla
    return pulla.__version__


add_keywords = dict(
    entry_points={
        'console_scripts': ['pulla = pulla.main:main'],
    }, )

fhan = open('requirements.txt', 'rU')
requires = [line.strip() for line in fhan.readlines()]
fhan.close()
#print('We require: ', requires)
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    fhan = open('README.txt')
    long_description = fhan.read()
    fhan.close()

setup(
    name='Pulla',
    description='Pulla helps you pull content from all repos in any folder',
    version=get_version(),
    packages=['pulla'],
    license='GPLv3+',
    author='Shubham Chaudhary',
    author_email='me@shubhamchaudhary.in',
    url='https://github.com/shubhamchaudhary/pulla',
    long_description=long_description,
    install_requires=requires, **add_keywords)
