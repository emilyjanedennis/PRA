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
- BrainPipe https://github.com/PrincetonUniversity/BrainPipe
- BrainRender https://www.biorxiv.org/content/10.1101/2020.02.23.961748v2
- Pisano _et al_ 2022 https://www.sciencedirect.com/science/article/pii/S2666166722001691

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

# Using raw lightsheet images to:

### 1. Make a stitched, whole-brain
#### If imaged on LaVision
If there are errors in these steps, usually it's
    1. regex needs to be edited
    2. elastix isn't installed properly (try `which elastix`) or is missing from bashrc
    3. terastitcher isn't installed properly (try `which terastitcher`) or is missing from bashrc
**things to do before running**
- edit run_tracing.py to poit to the appropriate directories and use the correct parameters for your imaging. especially pay attention to:
- systemdirectory
  - if you haven't edited directorydeterminer() appropriately, nothing will work
- inputdictionary
  - point to the raw images file, they should be in the format like
    `10-50-16_UltraII_raw_RawDataStack[00 x 00]_C00_xyz-Table Z0606_UltraII Filter0000.ome.tif`
  - if the format of your images differs, you'll need to edit the regex expression called in run_tracing (find it in tools/imageprocessing/preprocessing under `def regex_determiner`)
  - if you have more than one channel imaged in this folder, add channels. Examples:
    - one channel in the folder: `[["regch", "00"]]`
    - two chhannels in the folder `[["regch", "00"], ["cellch","01"]]`
- under params edit:
  - outputdirectory
        - give the path where you want things saved. I usually make it the animal's name (e.g. E001) and store temporarily in scratch `scratch/ejdennis/e001`   or more permanently ` /LightSheetData/brodyatlas/processed/e001`
  - xyz_scale
    - usually either (5,5,10) for data collected with the 1.3x objective or (1.63,1.63,10) if collected with the 4X objective
  - stitchingmethod
    - I keep this as "terastitcher"
  - AtlasFile
    - point to the file you want to register the brain to - usually this will be either the Waxholm MRI atlas `/jukebox/LightSheetData/brodyatlas/atlas/for_registration_to_lightsheet/WHS_SD_rat_T2star_v1.01_atlas.tif` or our atlas
  - annotationfile
    - the annotation file that describes the above brain, e.g. `/jukebox/LightSheetData/brodyatlas/atlas/for_registration_to_lightsheet/WHS_SD_rat_atlas_v3_annotation.tif`
  - resizefactor
    - usually 5 for 4x images, 3 for 1.3x images
  - slurmjobfactor
    - we keep this at 50, it's the number of files processed in step1 of run_tracing and slurm_files/step1.sh
  - transfertype
    - MAKE SURE THIS IS "copy" or else your data may get deleted, there are backups, but it's really annoying. Avoid at all costs, you can always clean up and delete things later.
  - you'll also want to check that in the __main__ run the systemdirectory points to your use case. For example, my scripts see if I'm running locally ("/home/emilyjanedennis/")

**to run**
if on spock, *after editing run_tracing.py*, go to your rat_BrainPipe folder, and run
    `sbatch slurm_scripts/step0.sh`
then go to your outputdirectory (e.g. /scratch/ejdennis/e001) that you specified in run_tracing.py
    `cd /scratch/ejdennis/e001`
there should now be a directory called lightsheet, go there
    `cd lightsheet`
run the pipeline from this folder (this is useful because it allows you to keep track of the exact parameters you used to run, and also parallelize by launching jobs for different brains at once on the cluster)
    `sbatch sub_registration.sh`

That's all! If everything runs successfully, you'll end up with a param_dict.p, LogFile.txt, two new resized tiffstacks, a mostly empty folder called injections, a folder called full_sizedatafld with the individual stitched z planes for each channel, and an elastix folder with the brains warped to the atlas defined in run_tracing.py AtlasFile

### 2. Make an atlas
If you have a group of stitched brains (e.g. e001/full_sizedatafld, e002/full_sizedatafld, and e003/full_sizedatafld), you can make an average brain for an atlas. Our rat atlas is for our lab, and therefore is made of only male (defined operationally by external genitalia) brains. However, we wanted to test our results and publish including female (similarly operationally defined) brains. Therefore we perfused, cleared, and imaged three female brains and created an atlas.

To make your own atlas, use the  `rat_atlas` folder.
  1. Edit `mk_ls_atl.sh` amd `cmpl_atl.sh` to use your preferred slurm SBATCH headings
  2. Edit `step1_make_atlas_from_lightsheet_images`
    - edit sys.path.append in the import section to reference your rat_BrainPipe cloned git repo
    - main section variables:
      - src should be where your folders (typically named by animal name, e.g. e001) live, these folders should each have full_sizedatafld folders in them
      - dst - where you want to save things. If you have a nested structure, make sure the parent structure exists (e.g.if you want to save in /jukebox/scratch/ejdennis/female_atlas/volumes, make sure /jukebox/scratch/ejdennis/female_atlas already exists)
      - brains should be the list of names of the brains you wish to use, corresponding to the names of the folders in dst that you want to average
  3. Run `sbatch --array=0-2 mk_ls_atl.sh` for three brains, --array=0-9 for 10 brains, etc.
  4. Edit `step2_compie_atlas.py`
    - edit sys.path.append in the import section to reference your rat_BrainPipe cloned git repo
    - edit main section variables:
      - src - should be the same as in step2
      - brains - should be the same as in step2
      - output_fld - should be a *different* folder than in step2: I like to place them in the same parent folder
      - parameterfld - this should point to a folder containing the affine/bspline transforms you want to use
  5. Run `sbatch --array=0-2 cmpl_atl.sh` for three brains, --array=0-9 for 10 brains, etc.
  6. Edit `step3_make_median.py`
    - edit the sys.path.append in the import section
    - in main, edit variables to match step2_compile_atlas
  7. Either locally or on the cluster head node (module load anacondapy/5.3.1), use export SLURM_ARRAY_TASK_ID=0, activate the lightsheet conda environment, and run `step3_make_median.py`


### 3. Put a brain in atlas space
if you have already "Made a stitched whole-brain", you may already have your brain in atlas space, depending on what you specified as the AtlasFile. If you have a tiff stack and you want to register it to an atlas file, you can use `elastix_to_pra.py`
    - change the mv to be your "moving image" (the brain tiffstack) and fx to your "fixed image" (the atlas volume)
    - change the output directory to where you want your elastix files and newly aligned tiff saved
   - change the outputfilename - this will be a resized mv file that is 140% the size of fx and is what is actually used for the alignment
