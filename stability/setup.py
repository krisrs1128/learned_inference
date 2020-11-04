import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="stability", # Replace with your own username
    version="0.0.0",
    author="Kris Sankaran",
    author_email="",
    description="Package for stability experiments",
    long_description="Package for stabiltiy experiments",
    long_description_content_type="text/markdown",
    url="https://github.com/krisrs1128/learned_inference",
    install_requires=required,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
