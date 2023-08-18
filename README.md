<p align="center">
  <img src="./docs/assets/imgs/logo.png" alt="datachart" height="300">
</p>

<p align="center">
<i>Data visualization package, simple to use, highly customizable</i>
<p>


---

**Documentation:** TODO

**Chart Examples:** https://github.com/eriknovak/datachart/tree/main/notebooks

**Source code:** https://github.com/eriknovak/datachart

---

# Datachart Python package

The datachart package is a python package for creating data visualizations. It is designed to be simple to use and highly customizable, i.e. it is easy to change the look and feel of the charts.

## Installation

TODO: create installation instructions

```bash
pip install datachart
```

## Usage Examples

Please find examples of how to use the package in the [notebooks](./notebooks) directory.


## Developer information

### ☑️ Requirements
Before starting the project make sure these requirements are available:
- [python][python]. The python programming language (v3.9 or higher).
- [git][git]. For versioning your code.


### 🛠️ Setup

#### Create the python environment

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

#### Install

To install the requirements run:

```bash
pip install -e .
```

#### Running tests

To run existing tests, simply run:

```bash
python -m unittest discover test
```


[python]: https://www.python.org/
[git]: https://git-scm.com/