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
3. If not at Princeton, install Elastix
    - see the end of this document for tips

## Data
Even our downsampled files are large, so we have deposited the main files you'll need at figshare here: https://figshare.com/articles/dataset/Princeton_RAtlas_PRA_/24207429
If you require the raw data (which is hundreds of Gb to some Tb per brain) email the authors and we will get you connected to Princeton IT to get a Globus link for accessing those data.

## Acknowledgements
This code builds heavily off of BrainPipe from Tom Pisano, Zahra Dahanderawala, and Austin Hoag. It also benefitted greatly from Nick Del Grosso and BrainGlobe.

## Citations
- Our protocol https://en.bio-protocol.org/en/bpdetail?id=4854&type=0 
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

### If on a local Ubuntu machine also install elastix (see section above), xvfb, Terastitcher:

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
- in `src/utils/io.py`, edit point to the appropriate directories and use the correct parameters for your imaging. especially pay attention to:
- line 125: systemdirectory
  - if you haven't edited directorydeterminer() appropriately, nothing will work. If at Princeton and running on spock, you do not need to change anything.

- in `src/utils/imageprocessing.py` point to the raw images file, they should be in the format like
    `10-50-16_UltraII_raw_RawDataStack[00 x 00]_C00_xyz-Table Z0606_UltraII Filter0000.ome.tif`
  - if the format of your images differs, you'll need to edit the regex expression in `utils/imageprocessing.py` under `def regex_determiner`, line 188. I found this https://www.dataquest.io/blog/regex-cheatsheet/ to be helpful.

**to run**
if you're on a local workstation, use


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
If you have a group of stitched brains (e.g. e001/full_sizedatafld, e002/full_sizedatafld, and e003/full_sizedatafld), you can make an average brain for an atlas. Our rat atlas is for our lab, and therefore is made of only male (defined operationally by external genitalia) brains. However, we wanted to test our results and publish including female (similarly operationally defined) brains. Therefore we perfused, cleared, and imaged four female brains and created an atlas.

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
- run general_elastix.sh example: `sbatch general_elastix.sh "/jukebox/brody/lightsheet/elastix_params/" "['/jukebox/brody/lightsheet/volumes/brain.tif']" "/jukebox/brody/lightsheet/atlasdir/PRA.tif" "/scratch/ejdennis/lightsheet" "1.4"` this will align brain.tif to PRA.tif using the parameter files in elastix_params and a multiplication value of 1.4. 1.4 means that the moving image (WHS_masked_atlas.tif) will be resized to 140% the size of the fixed image. This empirically works well for getting good alignments without too much fuss. Outputs will be saved in /scratch/ejdennis/lightsheet/brain_to_PRA
   4. check the alignment! If you have issues, try changing the WHS_masked_atlas.tif file (more cropping or changing intensity/depth of pixels, etc.) Read more in Elastix documentation. Usually this just works.

### 4. Put a third-party atlas/annotation into your atlas space (assuming PRA.tif for this description, and assuming you're using the Princeton cluster for examples, so edit files/paths accordingly for your system)
   0. Prep the files: you'll need an atlas file and an annotations file (atlas = looks like a brain, annotations = has a brain shape but has large chunks of it are different values, corresponding to brain regions). There also should be a labels file, usually a json or csv that tells you what the values in the annotations file mean. (e.g. value 10=olfactory bulb). Make sure the atlas and annotation files have these properties: (a) they are sagittally sectioned (b) have a black background (c) have approximately the same 'empty space' as your atlas (e.g. you don't want a huge amount of black/0s behind the spinal cord/cerebellum if that's not in your atlas space). and (d) mask any features not in your atlas. For example, for Waxholm Space Atlas (WHS) I used ImageJ BioFormat Importer to import the .nii files, reslice and transform to sagittal (with dorsal cortex on left) and crop. I did this for the annotations while recording a macro then applied that macro to the atlas file so they were treated identically, and then saved them as tiffs. I then used python to load the new sagittal annotation tif, set several values to 0 (like optic nerve, cochlea, etc that are not in our lightsheet-based PRA atlas) and saved out as WHS_masked_annotations.tif I then set all non-zero values to 1, and saved this as WHS_mask.tif. I then loaded the new sagittal atlas tiff, multiplied it by the WHS_mask, and saved as WHS_masked_atlas.tif.
   2. Make sure you have this repo cloned, and cd into PRA/src
   3. run general_elastix.sh example: `sbatch general_elastix.sh "/jukebox/brody/lightsheet/elastix_params/" "['/jukebox/brody/lightsheet/volumes/WHS_masked_atlas.tif']" "/jukebox/brody/lightsheet/atlasdir/PRA.tif" "/scratch/ejdennis/lightsheet" "1.4"` this will align WHS_masked_atlas.tif to PRA.tif using the parameter files in elastix_params and a multiplication value of 1.4. 1.4 means that the moving image (WHS_masked_atlas.tif) will be resized to 140% the size of the fixed image. This empirically works well for getting good alignments without too much fuss. Outputs will be saved in /scratch/ejdennis/lightsheet/WHS_masked_atlas_to_PRA
   4. check the alignment! If you have issues, try changing the WHS_masked_atlas.tif file (more cropping or changing intensity/depth of pixels, etc.) Read more in Elastix documentation. Usually this just works.
   5. run general_transformix.sh example: `sbatch general_transformix.sh "/jukebox/brody/lightsheet/volumes/WHS_masked_atlas_to_fPRA" "/jukebox/brody/lightsheet/atlasdir/fPRA.tif" "/jukebox/brody/lightsheet/volumes/WHS_masked_annotations.tif" "/scratch/ejdennis/lightsheet/WHS_$` this will use the Transform files in WHS_masked_atlas_to_PRA to transform WHS_masked_annotations.tif into PRA space
   6. check the alignment! If you have issues, make sure the resize/mult value is correct (checking the shape of resized.tif is a good first step, if mult = 1.4 (the default) then all axes should be 1.4x the atlas in all dimensions, and the same as the enlarged tiff created in step 3)

