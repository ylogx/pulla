from distutils.core import setup

def get_version():
    import pulla
    return pulla.__version__

def get_requirements():
    with open('requirements.txt', 'rU') as fhan:
        requires = [line.strip() for line in fhan.readlines()]
    return requires

def get_long_description():
    try:
        import pypandoc
        long_description = pypandoc.convert('README.md', 'rst')
    except (IOError, ImportError):
        with open('README.txt') as fhan:
            long_description = fhan.read()
    return long_description


add_keywords = dict(
    entry_points={
        'console_scripts': ['pulla = pulla.main:main'],
    }, )

setup(
    name='Pulla',
    description='Pulla helps you pull content from all repos in any folder',
    version=get_version(),
    packages=['pulla'],
    license='GPLv3+',
    author='Shubham Chaudhary',
    author_email='me@shubhamchaudhary.in',
    url='https://github.com/shubhamchaudhary/pulla',
    long_description=get_long_description(),
    install_requires=get_requirements(),
    **add_keywords)
