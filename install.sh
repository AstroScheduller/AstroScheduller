#!/bin/bash

# Begin of the script
echo "=========================="
echo "AstroScheduler Installer Script (v0.1)"
echo "=========================="

echo

# Type y to continue, n to exit
echo "This script will install AstroScheduler on your system."
echo "The following software packages will be required and installed:"
echo "  - wget"
echo "  - Go"
echo "  - Anaconda"
echo "  - Python"
echo "  - AstroScheduler"
echo "  - AstroScheduler Go Module"
echo "Do you want to continue? (y/n)"
read answer
if [ "$answer" != "y" ]; then
    echo "Exiting..."
    exit
fi

echo

# Check if Go is installed
if [ -z "$GOPATH" ]; then
  # If platform is Mac OS X
    if [ "$(uname)" = "Darwin" ]; then
        # Install Go - MacOS
        echo "Installing Go..."
        echo "=========================="
        brew install go
        echo "=========================="
        echo "Finished."
    fi
  # If platform is Linux
    if [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
        # Install Go - Linux
        echo "Installing Go..."
        echo "=========================="
        # Check if sudo is installed
        if [ -z "$(which sudo)" ]; then
            apt-get install -y golang
        else
            sudo apt-get install -y golang
        fi
        echo "=========================="
        echo "Finished."
    fi
fi

echo

# Check if Anaconda is installed
if [ -z "$CONDA_EXE" ]; then
  # If platform is Mac OS X
    if [ "$(uname)" = "Darwin" ]; then
        # Install Anaconda - MacOS
        echo "Installing Anaconda..."
        echo "=========================="
        brew install anaconda

        # Set Anaconda path
        export PATH="~/opt/anaconda3/bin:$PATH"
        echo "=========================="

        echo "Finished."
    fi
  # If platform is Linux
    if [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
        # Install Anaconda - Linux
        echo "Installing Anaconda..."
        echo "=========================="

        # Check if wget is installed
        if [ -z "$(which wget)" ]; then
            # Check if sudo is installed
            if [ -z "$(which sudo)" ]; then
                apt-get install -y wget
            else
                sudo apt-get install -y wget
            fi
        fi

        wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.3.1-Linux-x86_64.sh
        bash Anaconda3-5.3.1-Linux-x86_64.sh

        # Set Anaconda path
        export PATH="~/anaconda3/bin:$PATH"

        echo "=========================="
        echo "Finished."
    fi
fi

echo

# Check if Python is installed
if [ -z "$PYTHON_EXE" ]; then
  # If platform is Mac OS X
    if [ "$(uname)" = "Darwin" ]; then
        # Install Python - MacOS
        echo "Installing Python..."
        echo "=========================="
        brew install python
        echo "=========================="
        echo "Finished."
    fi
  # If platform is Linux
    if [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
        # Install Python - Linux
        echo "Installing Python..."
        echo "=========================="
        # Check if sudo is installed
        if [ -z "$(which sudo)" ]; then
            apt-get install -y python
        else
            sudo apt-get install -y python
        fi
        echo "=========================="
        echo "Finished."
    fi
fi

echo

# Install Python Package in ./setup.py
echo "Installing AstroScheduller Package..."
echo "=========================="
python setup.py install
echo "=========================="
echo "Finished."

echo

# Build AstroSchedullerGo Module
echo "Building AstroSchedullerGo Module..."
echo "=========================="
go build -o ./_scheduller.so ./*.go
echo "=========================="
echo "Finished."

echo

# Install AstroSchedullerGo Module
echo "Installing AstroSchedullerGo Module..."
echo "=========================="
python -c 'import astroscheduller as ash; ash.core().install("_scheduller.so")'
echo "=========================="
echo "Finished."

echo

# End of script
echo "=========================="
echo "Script finished."
echo "=========================="

