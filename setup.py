from distutils.core import setup


def get_version():
    return "0.3.0"


def get_requirements():
    with open("requirements.txt", "r") as fhan:
        requires = [line.strip() for line in fhan.readlines()]
    return requires


def get_long_description():
    try:
        import pypandoc

        long_description = pypandoc.convert_file("README.md", "rst")
    except (IOError, ImportError):
        with open("README.txt") as fhan:
            long_description = fhan.read()
    return long_description


add_keywords = dict(
    entry_points={
        "console_scripts": ["pulla = pulla.main:main"],
    },
)

setup(
    name="Pulla",
    description="Pulla helps you pull content from all repos in any folder",
    version=get_version(),
    packages=["pulla"],
    license="GPLv3+",
    author="Shubham Chaudhary",
    author_email="shubham@chaudhary.xyz",
    url="https://github.com/ylogx/pulla",
    long_description=get_long_description(),
    install_requires=get_requirements(),
    **add_keywords
)
