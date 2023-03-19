# PRA

## Purpose
The goals of this repo are:
1. Allow others to replicate our lightsheet manuscript
2. Allow non-Brody users to use and take advantage of these tools
3. Allow Brody lab members easy access to the tools developed and implemented on Priniceton's HPC spock

## To use
1. Clone this repo
2. Generate the lightsheet environment
   - in PRA, `conda env create -f environment.yaml`

3. Activate the ClearMap2 git module
    - To learn more aboud submodules, see [here](https://gist.github.com/gitaarik/8735255)
    - To make that code 'appear' in the repo use
    `git submodule update --init --recursive`
    to update it
    `git submodule update --recursive --remote`

4. If not at Princeton, install Elastix
    - see the end of this document for tips

## Acknowledgements
This code builds heavily off of BrainPipe from Tom Pisano, Zahra Dahanderawala, and Austin Hoag. It also benefitted greatly from Nick Del Grosso and BrainGlobe.

## Citations
- BrainPipe
- BrainGlobe
- Tom Pisano





## *INSTALLATION INSTRUCTIONS*:
* Note that this currently has only been tested on Linux (Ubuntu 16 and 18). SimpleElastix installation has also been tested in Windows 10 by Adrian.
* If on a cluster - Elastix needs to be compiled on the cluster - this was challenging for IT here and suspect it will be for your IT as well. If at Princeton, elastix is on spock


### Install simpleelastix

*_For Windows_*, Follow the instructions on [read the docs](https://simpleelastix.readthedocs.io/GettingStarted.html#compiling-on-windows).
Use the command line step (step 3) and skip the IDE steps 4 and 5.  If the Python wrapping fails, see this [known issue](https://github.com/SuperElastix/SimpleElastix/issues/243).

-------------
_*To install elastix on linux*_, follow the instructions in the manual under the easy way, not the "super easy" way

if you use the 'easy way' but have a modern computer, your gcc version may be too high. For this, you'll need at least ITK 5.0 which means you need to use elastix version 5, not 4.8. The following worked on Ubuntu 18 with two GeForce RTX 2070 SUPERs.

- made two dirs: ITK-build and elastix-build
- added ITKSNap 5
  file:///tmp/mozilla_emilyjanedennis0/InsightSoftwareGuide-Book1-5.1.0.pdf
  extracted downloaded .tar.gz and .tar.bz2 files to those directories
  in ITK-build, typed  `cmake ITK-build`
  then `sudo make install`
  in elastix-build, `cmake elastix-build` failed, so I went into the folder and found the CMakeFiles.txt
  `cd elastixfolder
  nano CMakeLists.txt`
  and added `list( APPEND CMAKE_PREFIX_PATH "/home/emilyjanedennis/Desktop/Apps/ITK-build/" )`

  note: I had to remove line 76 from `elastix-5.0.0/Components/Resamplers/MyStandardResampler/elxMyStandardResampler` which referred to an  undefined type called PointType which was throwing an exception during the make install process for elastix

[Download](https://github.com/abria/TeraStitcher/wiki/Binary-packages) TeraStitcher-installer. Move file to wherever you want Terastitcher to live, cd into that directory, and then:
```
$ bash TeraStitcher-Qt4-standalone-1.10.18-Linux
```
* Modify Path in ~/.bashrc:

```
export PATH="<path/to/software>/TeraStitcher-Qt4-standalone-1.10.18-Linux/bin:$PATH"
```
* Check to see if successful

```
$ which terastitcher
```


## Princeton-specific instructions
If on the cluster, and typing which terastitcher can't find terastitcher, try adding the following to your path

```
export PATH="/usr/people/pnilsadmin/TeraStitcher-Qt4-standalone-1.10.11-Linux/bin$PATH"
```

If on a local Ubuntu machine also install elastix (see section above), xvfb, Terastitcher:

```
$ sudo apt-get install xvfb
```
