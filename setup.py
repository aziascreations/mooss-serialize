from mooss.serialize.__version__ import VERSION
import setuptools

with open("README.md", "rb") as fh:
    long_description = fh.read().decode("utf-8")

setuptools.setup(
    name="mooss-serialize",
    version=VERSION,
    author="Herwin Bozet",
    author_email="herwin.bozet@gmail.com",
    maintainer="Herwin Bozet",
    maintainer_email="herwin.bozet@gmail.com",
    description="A Python package to help with serialization and deserialization of "
                "dataclasses through the help of a common interface while also insuring "
                "the parsed data is properly typed and handled in many situations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aziascreations/mooss-serialize",
    packages=setuptools.find_packages(),
    install_requires=[],
    extras_require={
        "dev": [
            "nose2>=0.11.0,<1.0.0",
            "semver>=2.13.0,<3.0.0",
            "check-manifest>=0.47,<1.0"
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires='>=3.9',
)
