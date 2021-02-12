import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "bit",
    version = "0.0.1",
    author = "Milind Murhekar",
    author_email = "milindmurhekar@gmail.com",
    description = "A small branch intigration tool",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires = '>=3.6',
    py_modules=['bit'],
    install_requires=[
        'Click',
        'colorama',
    ],
    entry_points='''
        [console_scripts]
        bit=main:cli
    ''',
)
