import setuptools

with open("readme.md", "r") as fh:
    long_description = fh.read()
    
with open("requirements.txt") as fh:
    required = fh.read().splitlines()

setuptools.setup(
    name="easyimputer",
    packages=['mvimpute'],
    version="0.0.1",
    author="FMR LLC",
    author_email="easyimputer@fmr.com",
    description="An abstract library for missing value imputation based on the amount of missing data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fidelity/easyimputer",
    install_requires=required,
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='missing_values impute imputation',
    
    project_urls={
        "Source": "https://github.com/fidelity/easyimputer"
    }
)