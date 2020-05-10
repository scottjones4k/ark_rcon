import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ark_rcon",
    version="0.0.4",
    author="Scott Jones",
    author_email="scott.jones4k@gmail.com",
    description="A basic RCON client for ARK servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scottjones4k/ark_rcon",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
