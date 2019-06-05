# pypirun

[![Build Status](https://cd.screwdriver.cd/pipelines/2852/badge)](https://cd.screwdriver.cd/pipelines/2852)
[![Codestyle](https://img.shields.io/badge/code%20style-pep8-lightgrey.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Code Coverage](https://codecov.io/gh/yahoo/pypirun/branch/master/graph/badge.svg)](https://codecov.io/gh/yahoo/pypirun)
[![Version](https://img.shields.io/pypi/v/pypirun.svg)](https://pypi.org/project/pypirun/)
[![License](https://img.shields.io/pypi/l/pypirun.svg)](https://pypi.org/project/pypirun/)
[![Wheel](https://img.shields.io/pypi/wheel/pypirun.svg)](https://pypi.org/project/pypirun/)

The **pypirun** command is a utility that allows running a python command line script from a python package, even if it is
not installed.  

## Table of contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Examples](#examples)
- [Contribute](#contribute)
- [License](#license)

## Background

This utility was written to allow CI/CD Pipeline templates to be able to function properly when run in docker containers that did not have the python utility needed already installed.

This allows the templates to continue to work in different docker containers without requiring redundant steps to install the needed python packages.

## Install

This package can be installed using the Python pip package manager.

In order to install this package the python environment must have:

* Python 3.6 or newer
* pip version 8.1.1 or higher
* setuptools 40.0.0 or higher

```console
$ pip install pypirun
```

## Usage

    usage: pypirun [-h] [--interpreter INTERPRETER] [--debug] [--always_install] package command ...
    
    positional arguments:
      package                    Comma seperated list of packages to install, this list cannot contain spaces
      command                    Command to run
    
    optional arguments:
      -h, --help                 show this help message and exit
      --interpreter INTERPRETER  Python interpreter to use
      --debug                    Enable debug output
      --always_install           Install the command even if it exists in the path
    
    Everything on the command line after the package name is executed in an environment with the package installed and on 
    the PATH.  As a result, the package and command must come after the optional arguments.
    
    By default pypirun will run the already installed command from the $PATH in the environment if it is found.  The
    --always_install flag will force it to install and run the command.

## Examples

### Run the serviceping utility from the python serviceping package

The following will run the command `serviceping -c 1 yahoo.com` from the [serviceping](https://pypi.org/project/serviceping/) package:

```console
dhubbard@mac:~$ pypirun serviceping serviceping -c 1 yahoo.com
SERVICEPING yahoo.com:80 (72.30.35.10:80).
from yahoo.com:80 (72.30.35.10:80): time=65.50 ms                                                                                                                                                                                                                 --- yahoo.com ping statistics ---
1 packages transmitted, 1 received, 0.0% package loss, time 73.038ms
rtt min/avg/max/dev = 65.50/65.50/65.50/0.00 ms
```

## Screwdriver V4 pypirun command

The pypirun package publishes a screwdriver v4 shared command called `python/pypirun`.

This command will set up python if it is not installed and install and run a the `pypirun` command line utility.

The following will run the command `serviceping -c 1 yahoo.com` from the [serviceping](https://pypi.org/project/serviceping/) package using the screwdriver sd-cmd:

```
sd-cmd python/pypirun@latest serviceping serviceping -c 1 yahoo.com
```

## Contribute

Please refer to [the contributing.md file](Contributing.md) for information about how to get involved. We welcome issues, questions, and pull requests. Pull Requests are welcome.

## Maintainers
Dwight Hubbard: dhubbard@verizonmedia.com

## License
This project is licensed under the terms of the [BSD](LICENSE-BSD) open source license. Please refer to [LICENSE](LICENSE) for the full terms.
