import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="stability", # Replace with your own username
    version="0.0.1",
    author="Kris Sankaran",
    author_email="test@test",
    description="Package for stability experiments",
    url="https://github.com/krisrs1128/learned_inference",
    install_requires=required,
    packages=setuptools.find_packages()
)
