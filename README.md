getHorizon
========================================
GetHorizon is a script to generate a horizon profile (skyline) from a viewpoint using Mapzen Elevation Service.
It has been developed in the framework of the class ["Renewable energy and solar architecture in Davos"](http://edu.epfl.ch/coursebook/fr/renewable-energy-and-solar-architecture-in-davos-PENS-210) offered at EPFL (Academic Year 2016-17) and of ongoing research at the [Laboratory of Integrated Performance in Design (LIPID)](http://lipid.epfl.ch/research/energy).

System requirements
---------------------
GetHorizon requires the following Python libraries:
- simplejson
- urllib
- polyline
- matplotlib
- numpy
- scipy

If they are not on your system please install them. It's easy with `pip` or `conda`.

### OS and Python version
  
Both Python 2 and Python 3 are supported on Windows and Mac, but the software has been mainly developed and tested on Windows with Python 3 distributed with Anaconda.

### Compiled version
  
You can easily obtain a standalone executable version of the scipt using [PyInstaller](http://www.pyinstaller.org/). In order to reduce the size of the executable, you might want to disable some libraries before compiling.

Usage and options
---------------------
To run the script, just execute:

```
python getHorizon.py
```
and follow the instructions on the terminal.

To use the script you need an API key from Mapzen. You can get yours from [here](https://mapzen.com/developers/sign_in). You have to insert the key in a text file called `API.txt` and save it in the same directory as the script.


Potential uses
---------------------

The data generated can be used as  input for different software and models intended for solar energy applications, such as:
- [CitySim](http://citysim.epfl.ch), for example through its interface [GHCitySim](https://github.com/gperonato/GHCitySim).
- [System Advisor Model (SAM)](https://sam.nrel.gov/)


Citation
---------------------
GetHorizon is free to use. You are kindly invited to acknowledge its use by citing it in a research paper you are writing, reports, and/or other applicable materials.
   
	@misc{peronato_gethorizon_2017,
		address = {Lausanne},
		title = {{getHorizon}},
		publisher = {Ecole polytechnique fédérale de Lausanne (EPFL),
		Laboratory of Integrated Performance in Design (LIPID)},
		author = {Peronato, Giuseppe},
		year = {2017}
	}


License
---------------------
getHorizon  
Copyright (c) 2017, Ecole polytechnique fédérale de Lausanne (EPFL)     
Laboratory of Integrated Performance in Design (LIPID)  

Developer: Giuseppe Peronato, giuseppe.peronato@epfl.ch


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.
* Neither the name of getHorizon nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 
@license BSD 3-clause "New" or "Revised" License <http://spdx.org/licenses/BSD-3-Clause>


### Mapzen Elevation Service
This script provides access to Mapzen Elevation Service.   
Mapzen services © [Mapzen](https://mapzen.com/), [OpenStreetMap](https://www.openstreetmap.org/copyright), and [others](https://mapzen.com/rights/#services-and-data-sources).   
Mapzen Elevation Service includes data from [NASA](https://www2.jpl.nasa.gov/srtm/), [USGS](https://topotools.cr.usgs.gov/gmted_viewer/), and [NOAA](https://www.ngdc.noaa.gov/mgg/global/global.html).   
Before using this tool, please make sure you understand and accept the conditions of use of Mapzen services:
https://mapzen.com/rights/


Useful links
---------------------
[Mapzen Elevation Service](https://mapzen.com/documentation/elevation/elevation-service/)


Contributors(a-z):
---------------------
[Giuseppe Peronato](https://github.com/gperonato)


Acknowledgments
---------------------
This script has been developed in the framework of the [ACTIVE INTERFACES](http://www.activeinterfaces.ch) research project, which is part of the National Research Programme "Energy Turnaround" (NRP 70) of the Swiss National Science Foundation (SNSF). Further information on the National Research Programme can be found at www.nrp70.ch.
