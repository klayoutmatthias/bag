# BAG (BAG AMS Generator)

BAG, a recursive acronym which stands for "BAG AMS Generator", is a fork and successor of
the [BAG\_framework](https://github.com/ucb-art/BAG_framework).

## Installation

### (Optional) Create Python Virtual Environment

Create a Python virtual environment:

```bash
python3 -m venv $HOME/.venvs/bag
```

Activate the virtual environment and set the environment variable telling BAG where to find Python.

```bash
activate $HOME/.venvs/bag/bin/activate
export PYBAG_PYTHON=$HOME/.venvs/bag/bin/python
```

### Install BAG

#### BAG

To install simply navigate to this directory and execute: 

```bash
python -m pip install .
```

#### PyBAG + CBAG + pybind11

To install the other required tools navigate to the `pybag` directory and execute:

```bash
python -m pip install . --log build.log
```

It is very possible that some debugging is required at this step due to the large C++ build stage.
The `build.log` can help in the debugging process.



## Licensing

This library is licensed under the Apache-2.0 license.  However, some source files are licensed
under both Apache-2.0 and BSD-3-Clause license, meaning that the user must comply with the
terms and conditions of both licenses.  See [here](LICENSE.BSD-3-Clause) for full text of the
BSD license, and [here](LICENSE.Apache-2.0) for full text of the Apache license.  See individual
files to check if they fall under Apache-2.0, or both Apache-2.0 and BSD-3-Clause.
