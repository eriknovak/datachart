---
title: Developer
---

# Development

This section is for developers only. It describes the requirements, the setup process, how to run tests, and how to deploy.

## ✅ Requirements
Before starting the project make sure these requirements are available:
- [python][python]. The python programming language (v3.9 or higher).
- [git][git]. For versioning your code.


## 🛠️ Setup

### Create the python environment

To create a python virtual environment using `venv`, simply run the following
commands:

```bash
# create a new virtual environment
python -m venv venv

# activate the environment (UNIX)
. ./venv/bin/activate

# activate the environment (WINDOWS)
./venv/Scripts/activate

# deactivate the environment (UNIX & WINDOWS)
deactivate
```

### Install

To install the requirements run:

```bash
pip install -e .[all]
```

## 🧪Tests

To run existing tests, simply run:

```bash
python -m unittest discover test
```

## 📦️ Build package

To build the package, run:

```bash
# upgrade the build package
python -m pip install --upgrade build

# build datachart package
python -m build
```

## 🚀 Deploy package

### Test PyPI

To deploy the package, run:

```bash
# upgrade the twine package
python -m pip install --upgrade twine

# deploy the datachart package to testpypi
python -m twine upload --repository testpypi dist/*
```

### Production PyPI

```bash
# upgrade the twine package
python -m pip install --upgrade twine

# deploy the datachart package to pypi
python -m twine upload dist/*
```


[python]: https://www.python.org/
[git]: https://git-scm.com/