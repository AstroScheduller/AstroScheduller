# Begin of the script
echo "=========================="
echo "AstroScheduler Installer Script (v0.1)"
echo "=========================="

# Ask if the user wants to install the program
echo "Do you want to install AstroScheduller?"
select yn in "Yes" "No"; do
    case $yn in
        Yes ) echo "Installing..."; break;;
        No ) exit;;
    esac
done


# Check if Go is installed
if [ -z "$GOPATH" ]; then
  # If platform is Mac OS X
    if [ "$(uname)" == "Darwin" ]; then
        # Install Go - MacOS
        echo "Installing Go..."
        echo "=========================="
        brew install go
        echo "=========================="
        echo "Finished."
    fi
  # If platform is Linux
    if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Install Go - Linux
        echo "Installing Go..."
        echo "=========================="
        sudo apt-get install -y golang
        echo "=========================="
        echo "Finished."
    fi
fi

# Check if Anaconda is installed
if [ -z "$CONDA_EXE" ]; then
  # If platform is Mac OS X
    if [ "$(uname)" == "Darwin" ]; then
        # Install Anaconda - MacOS
        echo "Installing Anaconda..."
        echo "=========================="
        brew install anaconda
        echo "=========================="
        echo "Finished."
    fi
  # If platform is Linux
    if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Install Anaconda - Linux
        echo "Installing Anaconda..."
        echo "=========================="
        sudo apt-get install -y anaconda
        echo "=========================="
        echo "Finished."
    fi
fi

# Check if Python is installed
if [ -z "$PYTHON_EXE" ]; then
  # If platform is Mac OS X
    if [ "$(uname)" == "Darwin" ]; then
        # Install Python - MacOS
        echo "Installing Python..."
        echo "=========================="
        brew install python
        echo "=========================="
        echo "Finished."
    fi
  # If platform is Linux
    if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        # Install Python - Linux
        echo "Installing Python..."
        echo "=========================="
        sudo apt-get install -y python
        echo "=========================="
        echo "Finished."
    fi
fi

# Install Python Package
echo "Installing AstroScheduller Package..."
echo "=========================="
python setup.py install
echo "=========================="
echo "Finished."

# Build AstroSchedullerGo Module
echo "Building AstroSchedullerGo Module..."
echo "=========================="
go build -o ./_scheduller.so ./*.go
echo "=========================="
echo "Finished."

# Install AstroSchedullerGo Module
echo "Installing AstroSchedullerGo Module..."
echo "=========================="
python -c 'import astroscheduller as ash; ash.core().install("_scheduller.so")'
echo "=========================="
echo "Finished."

# End of script
echo "=========================="
echo "Script finished."
echo "=========================="

