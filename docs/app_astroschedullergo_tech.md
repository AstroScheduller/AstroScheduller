![astro_scheduller](./docs/astro_scheduller.jpg)

# AstroSchedullerGo 0.9.3

[![](https://img.shields.io/badge/license-MIT-green)](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/LICENSE)
[![](https://img.shields.io/badge/release-v0.9.3-informational)](https://github.com/AstroScheduller/AstroScheduller/releases)
[![](https://img.shields.io/badge/其他文档语言-简体中文-orange)](./app_astroschedullergo_tech_CHN.md)

AstroScheduller project is trying to design an algorithm for generating astronomical observation plans. The project mostly designed in GoLang Code. AstroSchedullerGo was taken from a previous project [AstroScheduller.py](https://github.com/AstroScheduller/AstroScheduller).

## Get Start

#### Observation Parameters

The input of the AstroScheduller Program are observation parameters written in XML style. Here is an exmple with comments as below:

```xml
<scheduller>
    <observation>
        <duration>
            <begin>1627113420</begin> <!-- The timestamp of when the observation begins -->
            <end>1628113420</end> <!-- The timestamp of when the observation ends -->
        </duration>

        <telescope>
            <latitude>32.701500</latitude> <!-- The latitude of the telescope on Earth -->
            <longitude>-109.891284</longitude> <!-- The longitude of the telescope on Earth -->
            <altitude>3185</altitude> <!-- The altitude of the telescope on Earth -->
            <velocity>
                <ra>0.5</ra> <!-- The rotation speed of the telescope in R.A. direction -->
                <dec>0.6</dec> <!-- The rotation speed of the telescope in Dec. direction -->
            </velocity>
        </telescope>

        <elevation>
            <minimal>30</minimal> <!-- The lowest angle the telescope is able to operate -->
            <maximal>80</maximal> <!-- The highest angle the telescope is able to operate -->
        </elevation>

        <escape>
            <sun>20</sun> <!-- The smallest angle from the sun enable the telescope to operate -->
        </escape>
    </observation>

    <sources>
        <object> <!-- The first objects to be observed -->
            <identifier>PSR J1012+5307</identifier> <!-- The identifier of the object -->
            <ra>153.13930897</ra> <!-- The R.A. of the object (Unit: Degree) -->
            <dec>53.11737904</dec> <!-- The Dec. of the object (Unit: Degree) -->
            <duration>800</duration> <!-- Amount of time (in seconds) spending on observing the object -->
        </object>

        <object> <!-- The second objects to be observed -->
            <identifier>PSR B0320+39</identifier> <!-- The identifier of the object -->
            <ra>50.86090833</ra> <!-- The R.A. of the object (Unit: Degree) -->
            <dec>39.74802778</dec> <!-- The Dec. of the object (Unit: Degree) -->
            <duration>2400</duration> <!-- Amount of time (in seconds) spending on observing the object -->
            <weight>0.1</weight> <!-- The weight of the object, range from 0.0 to 1.0. Smaller weight is interpreted as less important. -->
			<important>1</important> <!-- The importance marker. The object will have a higher priority in the sorting, if is marked as 1. -->
        </object>
      
      	... <!-- More objects can be added -->
      
    </sources>
</scheduller>
```

If you already have a "Source List" for project [AstroScheduller.py](https://github.com/AstroScheduller/AstroScheduller), the list can be converted to the XML style observation parameters by [PyInterface.py](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/PyInterface.py). 

### Generate Observation Plans

1. Get a latest pre-built AstroSchedullerGo Program (or build a version based on the source code) from [releases](https://github.com/AstroScheduller/AstroScheduller/releases) after preparing a nice observation parameters. 

2. Open a new command line tools and switch to the current directory.

   ```bash
   cd /path/to/AstroSchedullerGo_v0_9_3_dev
   ```

3. Run the program by command `./AstroScheduller_vx_x_x_dev [PATH TO OBSERVATION PARAMETER.xml] [PATH TO EXPORT.xml]`.

   ```bash
   ./AstroSchedullerGo_v0_9_3_dev psr_list_debug.xml psr_list_debug_export.xml
   ```

4. The program will show `The schedule has been successfully generated.` upon the schedule is successfully generated. 

### PyInterface.py

[PyInterface.py](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/PyInterface.py) is a python script with class "scheduller()" can be used to run the program in a neat way. To use the script, Get a latest pre-built AstroSchedullerGo Program from [releases](https://github.com/AstroScheduller/AstroScheduller/releases) and save it in the same directory as the script. 

There are some scripts can be added after the declared class as below. 

1. Start a new scheduller class handle:

   ```
   schedullerHandle = scheduller()
   ```

2. Import parameters from XML style file: 

   ```python
   schedullerHandle.load_from_xml("./tests/psr_list_debug.xml")
   ```

   or, a "Source List" from project [AstroScheduller.py](https://github.com/AstroScheduller/AstroScheduller) can be also imported (or converted):

   ```python
   schedullerHandle.load_from_json("./tests/psr_list_debug.json")
   ```

3. Start to generate an observation plan:

   ```
   schedullerHandle.schedule()
   ```

   The script may ask you to specify the "core" to use (which means to specify which AstroSchedullerGo Program to use) if there are several of them available. 

4. Plot the generated plan:

   ```python
   schedullerHandle.plot()
   ```

5. Save the generated plan: 

   ```python
   schedullerHandle.save("./tests/psr_list_debug_schedule.xml")
   ```

   

There is an exmple available at the end of the [PyInterface.py](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/PyInterface.py). 

## License

AstroSchedullerGo is released as an open source project under the MIT license. See [LICENSE](https://github.com/AstroScheduller/AstroScheduller/blob/Dev/LICENSE) for more information. 

## Acknowledgement

We are deeply grateful to the researchers and students at the Shanghai Astronomical Observatory of the Chinese Academy of Sciences for their thoughtful discussions and works on testing the algorithm.


