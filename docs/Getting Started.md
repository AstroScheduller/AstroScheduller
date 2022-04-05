# Installation

## AstroScheduller Python Package

### Prerequisites

There are several python packages are required to run the AstroScheduller are listed below. All those packages are included in a standard Anaconda environment. 

 - numpy
 - matplotlib
 - requests

The `Astropy` Package is not required by the AstroScheduller. However, it is highly recommended to have it once, since several AstroScheduller functions are compatible with Astropy objects (such as coordinates and time objects). 


### Using setup.py

**Since the preview version of the AstroScheduller Package is not yet published into the PyPi, setup.py can be used to install the package.** 

Firstly clone the project from the Github before installing AstroScheduller with the setup.py:
``` shell
git clone https://github.com/xiawenke/AstroScheduller.git
```

Switch to the `AstroScheduller` directory:
``` shell
cd ./AstroScheduller
```

Run the installation:
``` shell
python setup.py install
```

Once the installation process is completed, you may test the package by the following commands to see if it works:
``` shell
(base) wenky@Wenkys-MacBook-Pro GitHub % python
Python 3.x.xx
Type "help", "copyright", "credits" or "license" for more information.
>>> import astroscheduller
>>>
```

So far you have finished with the Python part of the installation; the GoLang part of the AstroScheduller (called the `AstroSchedullerGo`) is not usually included in the Python package. The pre-build version of the AstroSchedullerGo Module is automatically downloaded from Github as the package has been imported if the internet is connected as well as **a pre-built version for the platform is available**. 

If errors such as *"The pre-build version of the AstroScheduller Module is not available"* and *"OSError: /xxx/xxx.so: invalid ELF header"* is reported, it means there is no pre-build module available for your platform. In this case, please see Install the AstroSchedullerGo Modules for more information.

## AstroSchedullerGo Modules

There are several pre-built versions of AstroSchedullerGo are provided, even though they are not guaranteed to perfectly work on all the devices and platforms. 

To check if a pre-build version of the module is available for your platform, use the following Python scripts: 

``` python
import astroscheduller as ash
ash.core().update()
```

The AstroSchedullerGo Module will be downloaded if a pre-build version is found; otherwise, an exception *"The pre-build version of the AstroScheduller Module is not available"* will be reported.  

### What if there is no pre-build version available for my platform? 

If you are unfortunately not to be provided with a pre-build version, you may need to compile the source code yourself. The compilation process will be easy if you already have a GoLang environment on your device. 

By using the following command to build the module:

```shell
cd /PATH/TO/ASTROSCHEDULLER/ && go build -buildmode=c-shared -o _scheduller.so ./*.go
```

Then, use the Python script below to install the module:

```python
import astroscheduller as ash
ash.core().install("/PATH/TO/ASTROSCHEDULLER/_scheduller.so")
```

For more instructions on how to compile your own AstroSchedullerGo Module (such as how to install a GoLang compiler), please refer to the Build From Source section. 

# Plan for the First Observation with AstroScheduller

Congratulations, you have now completed all the installation, and are ready to plan for yourself. fist observation with AstroScheduller. There is a quick example that demonstrates how the package works:

```python
import astroscheduller as ash                                # Import AstroScheduller

# Prepare for an example
ash.example("https://raw.githubusercontent.com/xiawenke/AstroScheduller/Dev/tests/psr_list_debug.xml")

obsPlan = ash.scheduller()                                   # Create a new scheduller object
obsPlan.objects.from_xml("./example.xml")                    # Load the objects from a XML file
obsPlan.get_schedule()                                       # Generate the schedule
obsPlan.stats()                                              # Calculate the statistics
obsPlan.plot().show()                                        # Plot the schedule
obsPlan.schedule.to_table("./example.txt")                   # Export the schedule to a table
```

In this example, a pre-prepared XML format file is read and automatically planned. In the end, the planning results are presented in three different formats: some stats, a plot, and a table. 

In addition to importing XML format files, AstroScheduller also supports some more flexible ways of importing objects to be observed -- it's much more powerful than this simple demonstration. To go further, please see other examples or later chapters. 