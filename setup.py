"""maillinter uses setuptools based setup script.

For the easiest installation type the command:

    python3 setup.py install

In case you do not have root privileges use the following command instead:

    python3 setup.py install --user

This installs the library and automatically handle the dependencies.
"""
import os

import setuptools

base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, 'src')

about = {}
with open(os.path.join(src_dir, 'maillinter', '__about__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, "README.md")) as f:
    long_description = f.read()

setuptools.setup(
    name=about['__title__'],
    use_scm_version=True,
    url=about['__uri__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__email__'],
    description=about['__summary__'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packaged=setuptools.find_packages(where='src'),
    setup_requires=['setuptools_scm'],
    install_requires=['setuptools_scm', 'pyperclip', 'pip-tools'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Email',
    ],
)
