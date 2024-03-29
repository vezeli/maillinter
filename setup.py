"""maillinter uses setuptools based setup script.

For the easiest installation type the command:

    python3 setup.py install

In case you do not have root privileges use the following command instead:

    python3 setup.py install --user

This installs the library and automatically handle the dependencies.
"""
import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="maillinter",
    use_scm_version={"write_to": "src/maillinter/_version.py"},
    description="The e-mail content formatter.",
    long_description=long_description,
    keywords="automation mail linter formatting",
    author="Velibor Zeli",
    author_email="zeli.velibor@gmail.com",
    url="https://github.com/vezeli/maillinter",
    license="MIT",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    setup_requires=["setuptools_scm"],
    install_requires=["nltk", "pyperclip", "setuptools_scm"],
    entry_points={"console_scripts": ["maillinter = maillinter.scripts.__main__:cli"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Topic :: Communications :: Email",
    ],
)
