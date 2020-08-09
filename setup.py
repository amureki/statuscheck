import codecs
from os.path import abspath, dirname, join

from setuptools import find_packages, setup

here = abspath(dirname(__file__))

with codecs.open(join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

about = {}

with open(join(here, "statuscheck", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    author=about["__author__"],
    author_email=about["__email__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Tool to check PaaS/SaaS status pages",
    entry_points={"console_scripts": ["statuscheck=statuscheck.cli:main"]},
    install_requires=open(join(here, "requirements.txt")).readlines(),
    extras_require={"tests": ["coverage", "pytest", "respx"]},
    license="Apache Software License 2.0",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="statuscheck",
    name="statuscheck",
    packages=find_packages(exclude=["tests", "tests.*"]),
    url=about["__url__"],
    version=about["__version__"],
    zip_safe=False,
)
