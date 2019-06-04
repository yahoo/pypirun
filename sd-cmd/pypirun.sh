#!/usr/bin/env bash
# Copyright 2019, Oath Inc.
# Licensed under the terms of the BSD 3 Clause license. See LICENSE file in project root for terms.
# This script bootstraps the pypirun command line utility.
#
# This command will handle bootstrapping the following:
# - A python 3.x interpreter
# - The Python package manager utility (pip)
# - The ouroath.pypirun utility
#
# Once everything is bootstrapped, it will run the pypirun command line utility
# passing all command line arguments to it.
#
# The bootstrapping code can bootstrap Redhat/Fedora/Centos, Debian/Ubuntu
# and Alpine environments.

set -e
PYTHON_VERSION="`python3 --version 2>/dev/null`" || true
export PATH=$PATH:~/.local/bin

function install_python {
    if [ "$PYTHON_VERSION" != "" ]; then
        return 0
    fi
    if [ -e "/usr/bin/yum" ]; then
        grep Fedora /etc/redhat-release 2>/dev/null || RC="$?"
        if [ "$RC" = "0" ]; then
            yum install -y sudo python3-pip
        else
            if [ ! -e "/usr/bin/yum-config-manager" ]; then
                sudo -E yum install -y yum-utils
            fi
            if [ ! -e "/etc/yum.repos.d/python_rpms.repo" ]; then
                sudo -E yum-config-manager --add-repo https://edge.artifactory.yahoo.com:4443/artifactory/python_rpms/python_rpms.repo
            fi
            if [ ! -e "/opt/python/bin/python3.6" ]; then
                sudo -E yum install -y yahoo_python36
            fi
            export PATH=$PATH:/opt/python/bin
        fi
    fi
    if [ -e "/usr/bin/apt-get" ]; then
        sudo -E apt-get install -y python3 python3-venv
    fi
    if [ -e "/sbin/apk" ]; then
        sudo -E apk add python3
    fi
}

function python_bin_dir {
    python3 -c 'import os,sys;print(os.path.dirname(sys.executable))'
}

function install_pyrun {
    if [ ! -e "`python_bin_dir`/pypirun" ]; then
        python3 -m pip install -q --user --index-url=https://edge.dist.yahoo.com:4443/artifactory/api/pypi/pypi/simple ouroath.pyrun 2> /dev/null
    fi
}

function pyrun_command {
    set +e
    PYRUN_COMMAND="`which pypirun 2>&1`"
    set -e
    if [ "$PYRUN_COMMAND" = "" ]; then
        if [ -e "~/.local/bin/pypirun" ]; then
            PYRUN_COMMAND="~/.local/bin/pypirun"
        fi
    fi
}

install_python
install_pyrun
pypirun $@
