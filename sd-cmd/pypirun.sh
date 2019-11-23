#!/usr/bin/env bash
# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
# This script bootstraps the pypirun command line utility.
#
# This command will handle bootstrapping the following:
# - A python 3.x interpreter
# - The Python package manager utility (pip)
# - The pypirun utility
#
# Once everything is bootstrapped, it will run the pypirun command line utility
# passing all command line arguments to it.
#
# The bootstrapping code can bootstrap Fedora, Debian/Ubuntu
# and Alpine environments.

# set -e
export PATH=$PATH:/opt/python/cp38-cp38m/bin:/opt/python/cp37-cp37m/bin:/opt/python/cp36-cp36m/bin:/opt/python/cp35-cp35m/bin:/opt/python/bin:/usr/local/bin:~/.local/bin
VERSION="`python3 -c "import pip,sys,venv;print(str(sys.version_info.major)+'.'+str(sys.version_info.minor))" 2>/dev/null`"
RC="$?"
if [ "$RC" != "0" ]; then
    PYTHON_VERSION=""
fi

function install_python {
    if [ "$PYTHON_VERSION" != "" ]; then
        return 0
    fi
    if [ -e "/usr/bin/yum" ]; then
        yum install -y python3-pip python3-devel python3 which > /dev/null 2>&1
        return 0
    fi
    if [ -e "/usr/bin/apt-get" ]; then
        apt-get install -y python3 python3-venv python3-pip > /dev/null 2>&1
        return 0
    fi
    if [ -e "/sbin/apk" ]; then
         apk --update add python3 python3-dev py3-pip py3-cffi py3-cparser py3-openssl py3-lxml gcc musl-dev libc-dev libffi libffi-dev libxml2-dev libxslt-dev openssl openssl-dev ca-certificates > /dev/null 2>&1
         return 0
    fi
}

function python_bin_dir {
    python3 -c 'import os,sys;print(os.path.dirname(sys.executable))'
}

function install_pyrun {
    python -m pypirun.utility 2>/dev/null
    RC="$?"
    if [ "$RC" != "0" ]; then
        python3 -m pip install -q pypirun 2> /dev/null
    fi
}

function pyrun_command {
    PYRUN_COMMAND="`which pypirun 2>&1`" || RC="$?"
    if [ "$PYRUN_COMMAND" = "" ]; then
        if [ -e "~/.local/bin/pypirun" ]; then
            PYRUN_COMMAND="~/.local/bin/pypirun"
        fi
    fi
}

function ensure_venv_works {
    python3 -m venv --clear /tmp/foo > /dev/null 2>&1
    RC="$?"
    if [ "$RC" = "1" ]; then
        PYTHON_VERSION=""
        install_python
    fi
    python3 -m venv /tmp/foo > /dev/null 2>&1
    RC="$?"
    if [ "$RC" = "1" ]; then
        echo "Unable to install a Python interpreter with a working venv module"
        exit 1
    fi
}

install_python
ensure_venv_works
install_pyrun
python3 -m pypirun $@
