![astro_scheduller](https://raw.githubusercontent.com/AstroScheduller/AstroScheduller/Dev/docs/astro_scheduller.jpg)

# AstroScheduller 1.0.x

[![](https://img.shields.io/badge/license-MIT-green)](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/LICENSE)
[![](https://img.shields.io/badge/release-v0.9.3-informational)](https://github.com/AstroScheduller/AstroScheduller/releases)
[![](https://img.shields.io/badge/python-3.6+-orange)]()
[![CodeQL](https://github.com/AstroScheduller/AstroScheduller/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/AstroScheduller/AstroScheduller/actions/workflows/codeql-analysis.yml)

The AstroScheduller project is developing a user-friendly Python package with an algorithm for planning astronomical observations. This project was taken from a previous project [AstroScheduller.py](https://github.com/AstroScheduller/AstroSchedullerPy).

Using PiPI to install:

The most recent stable version of  AstroScheduller Package is available on PyPI. Using the following command to install the package and the required packages will automatically be installed: 

```bash
pip install AstroScheduller
```

If you already have an older version of AstroScheduller installed, as AstroScheduller is currently in active update, we strongly recommend that you often update the package as follows

```{shell}]
pip install --upgrade astroscheduller
```

The AstroScheduller GUI uses a package called [Tkinter](https://tkdocs.com/tutorial/install.html), which is required since AstroScheduller v1.0.0. **This package will not be able to install automatically by PyPI. **If you are using the [Anaconda](https://www.anaconda.com), the Tkinter Package might be included in the distribution. To check if Tkinter has been already installed, try the following: 

```{shell}
Python 3.8.10 | packaged by conda-forge 
Type "help", "copyright", "credits" or "license" for more information.
>>> import tkinter
```

If Tkinter is not installed, an exception will be thrown. Then, **the Tkinter installation would be as the following**: 

```{shell}
# For Ubuntu: 
sudo apt-get update && sudo apt-get install python3-tk

# For MacOS: 
## You should first install the Homebrew software, then install the Tkinter. 
## Using the command as follows: 
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" && brew install python-tk
```

For more information about the installation, see [Getting Started: Installation](https://astroscheduller.github.io/tutorials-docs/getting-started.html#installation)

## Demo on Google Colab: 
 - [Introduction to AstroScheduller](https://colab.research.google.com/drive/1pnGP9p53ELxzyRdV7aMAa21Q0RGHIbaM?usp=sharing)
 - [AstroScheduller Examples](https://colab.research.google.com/drive/1fHDBcop4ZaMf3P7huPEB-w_y5VkIsI2X?usp=sharing)

## Documentations

 - [AstroScheduller Documentation Homepage](https://astroscheduller.github.io/)
 - [Appendix: Technical Documentation for AstroSchedullerGo](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/docs/app_astroschedullergo_tech.md)

## To-do

See [todo.md](./docs/todo.md). 

## License

The AstroScheduller Project and AstroSchedullerGo are released as open source projects under the MIT license. See [LICENSE](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/LICENSE) for more information. 

## Acknowledgement

We are deeply grateful to the researchers and students at the Shanghai Astronomical Observatory of the Chinese Academy of Sciences for their thoughtful discussions and work on testing the algorithm.
