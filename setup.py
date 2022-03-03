from mooss.serialize.__version__ import VERSION
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mooss-serialize",
    version=VERSION,
    author="Herwin Bozet",
    author_email="herwin.bozet@gmail.com",
    description="Test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://localhost/",
    packages=setuptools.find_packages(),
    install_requires=[
        'mooss-core>=0.0.1',
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    python_requires='>=3.9',
)
