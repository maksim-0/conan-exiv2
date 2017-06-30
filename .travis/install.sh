#!/bin/bash

set -e
set -x

if [[ "$(uname -s)" == 'Darwin' ]]; then
    brew update || brew update
    brew outdated pyenv || brew upgrade pyenv
    brew install pyenv-virtualenv
    brew install cmake || brew upgrade cmake

    if which pyenv > /dev/null; then
        eval "$(pyenv init -)"
    fi

    pyenv install 2.7.10
    pyenv virtualenv 2.7.10 conan
    pyenv rehash
    pyenv activate conan
else
    mkdir $HOME/usr
    export PATH="$HOME/usr/bin:$PATH"
    wget https://cmake.org/files/v3.8/cmake-3.8.2-Linux-x86_64.sh
    chmod +x cmake-3.8.2-Linux-x86_64.sh
    ./cmake-3.8.2-Linux-x86_64.sh --prefix=$HOME/usr --exclude-subdir --skip-license
fi

pip install conan --upgrade
pip install conan_package_tools

conan user
