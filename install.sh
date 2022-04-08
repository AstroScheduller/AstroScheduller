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

echo "Installing Go..."
# If platform is Mac OS X
if [ "$(uname)" = "Darwin" ]; then
    # Install Go - MacOS
    echo "=========================="
    brew install go
    echo "=========================="
    echo "Finished."
fi
# If platform is Linux
if [ "$(expr substr $(uname -s) 1 5)" = "Linux" ]; then
    # Install Go - Linux
    echo "=========================="
    # Check if sudo is installed
    if [ -z "$(which sudo)" ]; then
        sudo apt-get install -y golang
    else
        apt-get install -y golang
    fi
    echo "=========================="
    echo "Finished."
fi

echo

# Check if Python is installed
echo "Installing Anaconda..."
if [ -z "$python3" ]; then
    echo "Python is installed. Skipped."
else
    echo ""
    echo "==================== INSTRUCTIONS ===================="
    echo "1. Press ENTER when Anaconda Installer asks following: "
    echo "> Anaconda3 will now be installed into this location:"
    echo "> /root/anaconda3"
    echo ""
    echo "2. Type 'yes' when Anaconda Installer asks following: "
    echo "> Do you wish the installer to initialize Anaconda3 "
    echo "> in your /root/.bashrc ? [yes|no]"
    echo "======================================================="
    echo ""

    # Press enter to continue
    echo "Press ENTER to continue install Anaconda..."
    read answer

  # If platform is Mac OS X
    if [ "$(uname)" = "Darwin" ]; then
        # Install Anaconda - MacOS
        echo "Installing Anaconda..."
        echo "=========================="
        wget https://repo.anaconda.com/archive/Anaconda3-2021.11-MacOSX-x86_64.pkg
        bash Anaconda3-2021.11-MacOSX-x86_64.pkg

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
        if [ -z "$(wget)" ]; then
            echo "wget is detected. Skipped."
        else
            # Check if sudo is installed
            if [ -z "$(which sudo)" ]; then
                sudo apt-get install -y wget
            else
                apt-get install -y wget
            fi
        fi

        wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
        bash Anaconda3-5.3.1-Linux-x86_64.sh

        # Set Anaconda path
        export PATH="~/anaconda3/bin:$PATH"

        echo "=========================="
        echo "Finished."
    fi
fi

echo

# Install Python Package in ./setup.py
echo "Installing AstroScheduller Package..."
echo "=========================="

if [ -z "$(which sudo)" ]; then
    sudo apt-get install -y python3-pip
else
    apt-get install -y python3-pip
fi

# Install AstroScheduler
pip install ./
pip3 install ./
echo "=========================="
echo "Finished."

echo

# Build AstroSchedullerGo Module
echo "Building AstroSchedullerGo Module..."
echo "=========================="
go build -buildmode=c-shared -o ./_scheduller.so ./*.go
echo "=========================="
echo "Finished."

echo

# Install AstroSchedullerGo Module
echo "Installing AstroSchedullerGo Module..."
echo "=========================="
cd ../
python -c 'import astroscheduller as ash; ash.core().install("./AstroScheduller/_scheduller.so")'
python3 -c 'import astroscheduller as ash; ash.core().install("./AstroScheduller/_scheduller.so")'
echo "=========================="
echo "Finished."

echo

# End of script
echo "=========================="
echo "Script finished."
echo "=========================="

