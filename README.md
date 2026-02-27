# cleared_brains

## Purpose
The goals of this repo are:
1. to build on PRA repo, which produced the 2024 Dennis et al manuscript
2. include new tools and documentation as environments/processes evolve
3. share with our collaborators and later the public as we produce manuscripts

## To use
1. Clone this repo
2. Make sure you have mamba (or conda if you prefer, if so, replace mamba with conda throughout)

If you're not at Janelia, you'll need to make sure you have mamba or conda installed, e.g. with [miniconda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh) and know that path, make sure to 

At Janelia:
- log in to login1 or login2
- start an interactive node 
  bsub -Is -W 04:00 -n 1 /bin/bash
- install [miniconda](https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh) 
  - Janelia specific instructions can be found on the wiki [here](https://hhmi.atlassian.net/wiki/spaces/AL/pages/156205218/Data+processing+with+Python+on+the+Janelia+Compute+Cluster?atlOrigin=eyJpIjoiMjQ3ZTVkMGZmOGMxNGE0ZDhkNDVjZDUxODJiMDMzYmQiLCJwIjoiY29uZmx1ZW5jZS1jaGF0cy1pbnQifQ)
- add to path (change /path/to/your/directory below to the actual path to your directory)
export PATH="$PATH:/path/to/your/directory"
- from the this repo:
  mamba env create -f environment.yaml
  conda activate clearedbrains
- check path:
  which python
- it should say ~/miniforge3/envs/clearedbrains...

3. Generate the environment
  - in the repo folder, `mamba env create -f environment.yaml` this will create an environment called clearedbrains
4. Decide if you'll use [ClearMap2](https://www.cellularimaging.org/blog/blog-post-title-one-28kxw) and [BigStitcher-Spark](https://github.com/JaneliaSciComp/BigStitcher-Spark?tab=readme-ov-file#install). If so, install those, you'll need the paths for the next steps!
   - BigStitcher-Spark is what we use to take our multi-tile imaging, turn it into a .zarr file which we later turn into (giant) individual tiff files of each slice the whole brain. ClearMap2 just receives the tiffs created from this fused image.
   - ClearMap2 is what we use for finding cell centers, like Arc and cFos. Several alternatives exist, like custom 3d UNets or BrainRender's cellfinder. If you use another tool to find cell centers and you want to use points transformix tools from here, you need to make sure your outputs have the same structure: a csv file with the headers ['x','y','z']. Else, you'll need to change the pre_transformix.py script to adjust to your data formats.
 
cd $CLEARED_BRAINS_FLD
cd src
5. Update the src/config_file.sh file with all the relevant paths, commenting out anything you don't need as described in the file
6. try running ./test_config.sh It should open a python instance. Type exit() and enter to leave python.

## Data
Even downsampled files are large, so we have deposited the main files can be found here:

- rat data from the Princeton Ratlas (PRA) manuscript can be found [here](https://figshare.com/articles/dataset/Princeton_RAtlas_PRA_/24207429)
- _Mus caroli_ files can be found [here](link)

## Acknowledgements
This code builds off of PRA, which built heavily off of BrainPipe from Tom Pisano, Zahra Dahanerawala, and Austin Hoag. It also benefitted greatly from Nick Del Grosso and BrainGlobe. Thanks also to Nishan Shettigar and Alison Comrie for suggestions to improve the code.

## Citations
- Our [PRA protocol](https://en.bio-protocol.org/en/bpdetail?id=4854&type=0) for whole, cleared rat brains and alignments
- [PRA](https://github.com/emilyjanedennis/PRA/)
- [BrainPipe](https://github.com/PrincetonUniversity/BrainPipe)
- [BrainRender](https://www.biorxiv.org/content/10.1101/2020.02.23.961748v2)
- [Pisano _et al_ 2022](https://www.sciencedirect.com/science/article/pii/S2666166722001691)

# Using lightsheet images to:

### 1. Make a stitched, whole-brain
TODO: add Nishan's processing steps as command line code

- use 1_fuse_volume.sh and provide a single input: a full path to the processed/bigstitcher folder created above. e.g.
`./1_fuse_volume.sh "/path/to/brain/processed/bigstitcher`

We expect your files to be in the same format as ours: you should have a folder containing
- a folder called interestpoints.n5
- dataset.h5
- dataset.xml
- an output file ending in .tif, e.g. 2025-01-15_123328_fused_12.tif

you may have additional dataset.xml files, e.g. 
- dataset.xml~1
- dataset.xml~2
- dataset.xml~3

### 2. Make an atlas

#### General procedure
- generally we use a strategy described in our [PRA protocol](https://en.bio-protocol.org/en/bpdetail?id=4854&type=0). Briefly:
  1. we first align pairs of brains, then take a median of the aligned image (mv, for moving image) and the brain it was aligned to (fx, for fixed image), and continue until we get one average brain. This creates a "seed" image
  2. Align all of the individual brains to the seed, take the median of the aligned brains+seed, and create a new seed, "seed1"
  3. Repeat step 2, making "seed2"
  4. Repeat step 2, making "seed3"
  5. Repeat step 2, making a "pre_final" median
  6. Open FIJI, open Plugins/Macros/Record and then then adjust the image in FIJI to be centered in all axes and have a similar amount of blank/black space around the brain volume.
  7. Save the adjusted brain as your new CCF (e.g. "caroli.tif") and save the macro as a record of what manipulations were done (e.g. "caroli_prefinal-to-final.txt")

  Please see the FIJI tips under Helpful Extras

#### To run a paired alignment (step 1) use
`./atlas_elastix.sh MV_VOL FX_VOL OUTPUT_DIR`
where MV_VOL is a full path to your moving volume, the image you want to align to the fixed volume e.g.
`./atlas_elastix.sh /path/to/folder/male1.tif /path/to/folder/female1.tif /path/to/output/folder`

#### To make a median of two or more brains (they MUST be the same shape) e.g. the end of step 1-5 after alignments complete
`./atlas_median.sh LIST_OF_BRAINS OUTPUT_DIR` and optionally `OUTPUT_TIF` where LIST_OF_BRAINS is a parenthetical contatining full paths to the images you'd like to take a median of... take care to make sure you're using the alignment OUTPUT from mv->fx in step 1 and the fx from step 1, e.g. ("path/to/brain1_in-brain2-space.tif" "path/to/brain2.tif"), OUTPUT_DIR is a full path to a directory where you'd like the median to be stored, and you can optionally provide the full path of the tiff file you'd like to save. e.g.
`./atlas_median.sh ("/path/to/brain1_in_seed1_space.tif" "/path/to/brain2_in_seed1_space.tif" "/path/to/brain3_in_seed1_space.tif" "/path/to/brain4_in_seed1_space.tif") "/path/to/output/fld" "/path/to/output/fld/seed2.tif"`

### 3. Put a brain in atlas space
- align your brain to the atlas CCF using 0_elastix_run.sh:
`./0_elastix_run.sh MV_VOL FX_VOL OUTPUT_DIR` where MV_VOL is the brain volume, FX_VOL is the CCF you want to align your brain to, OUTPUT_DIR is where you'd like the Transform files to be saved to 
`./0_elastix_run.sh /path/to/mybrain.tif /path/to/CCF.tif /path/to/output/dir`
- To evaluate the outcome, see FIJI tips below in "Helpful Extras" for viewing outputs. Briefly, open the CCF and the tif created in the output dir, e.g. /path/to/output/dir/mybrain_in_CCF.tif and use Image/Color/Merge Channels and select both the CCF.tif and mybrain_in_CCF.tif You may want to use Image/Adjust/Brightness/Contrast to adjust the brightness of each image. They should be overlaid and well-aligned. You can also open an annotation file for your CCF in this way and see the labels on your brain.

### 4. Use Transformix

#### 4.1 Transform an image
After running elastix with brainA.tif (mv) to CCF.tif (fx), you can use these TransformParameters files and apply the exact same transformation on any image of the same size as your mv. The most common use case is for visualizing the alignment process by applying the same transformation to a 'grid' volume and showing how the image was warped. 

To do this use
`./X_transformix_images.sh TRANSFORMS_FLD MV_VOL OUTPUT_FILE` where the TRANSFORMS_FLD is the folder produced by elastix aligning your mv to your fx volume, MV_VOL is the new image/volume that you want to apply the transforms to. This MUST be the exact same dimensions as the image used for elastix. OUTPUT_FILE is where you'd like the new image saved.
e.g. if you ran 
`./0_elastix_run.sh /path/to/brainA.tif /path/to/CCF.tif /path/to/output_dir` 
and the dimensions of brainA.tif are (100,300,200). You make a volume that is just a 3d grid (/path/to/grid.tif) and has dimensions of (100,300,200), and want to visualize how 'wavy' the grid looks. Run:
`./X_transformix_images.sh /path/to/output_dir /path/to/grid.tif /path/to/output/grid_in_CCF.tif`


#### 4.2 Transform a set of points
Remember, transformix for points is "backwards"... to get points from your volume into a CCF, you should be using TransformParameter files made by using elastix to align the CCF (mv) _*to*_ your volume (fx) with points/cells. The [elastix manual](https://www2.imm.dtu.dk/courses/02503/docs/elastix-5.2.0-manual.pdf) is very useful for understanding this! 

e.g. If you ran 
`./0_elastix_run.sh /path/to/CCF.tif /path/to/brainA.tif /path/to/transforms_output_dir` NOTE THE DIFFERENCE FROM 5.1's EXAMPLE
and you have points in brainA.tif coordinates that you want in CCF.tif coordinates, run:
`./5_transformix_cells.sh TRANSFORMS_FLD TXT_FILE MV_VOL OUTPUT_DIR` for example
`./5_transformix_cells.sh /path/to/transforms_output_dir /path/to/filtered_cells_for-transformix.txt /path/to/brainA.tif /path/to/cells_output_dir`

- if you produced a csv of points called filtered_cells.csv with heading (z,y,x), you'll also need to run 
`pre_transformix.py DIRECTORY_WITH_CSV` where DIRECTORY_WITH_CSV is the directory containing filtered_cells.csv

  points formatted for transformix in a .txt file:
      point  
      134682  
      3 3 29
      4 3 34
      5 3 48
      6 3 51
      8 3 48

# TODO DOUBLE CHECK THE ORDER IS ZYX
  same file as a csv:
      ,z,y,x
      0,3,3,29
      1,4,3,34
      2,5,3,48
      3,6,3,51


### 5. Put a third-party atlas/annotation into your CCF (Common Coordinate Framework) 
- align the third-party CCF to your CCF (see 3. Put a brain in atlas space, above) e.g.
`./0_elastix_run.sh /path/to/third-party-CCF.tif /path/to/yourCCF.tif /path/to/output/thirdparty_in_yourCCF`
- transform the annotation into your CCF using the elastix output (TransformParameters), see (4.1 Transform an image above)
`./`

### 6. Do all the things: Start with BigStitcher's output, run ClearMap2, and get the cells in CCF (allen atlas) space:
- **SIMPLEST IF AT JANELIA**: 
  - update runbybasename.sh line 8 to fit your data path structure
  - make sure all lines are un-commented in superscript_all.sh and then 
  - cd into cleared_brains/src
  - run:
`./runbybasename.sh "2025-01-01_11111"`

- ELSEWHERE: 
  - Elastix (step 0) must _finish_ before transformix can run, otherwise all steps go in numerical order (1, 2, 3_1, 3_2, 3_3, 4, 5, 6). You can use the superscript_all.sh as a guide, and run commands in that order with those inputs on your local machine or cluster, adjusted for your scheduler and paths.

# Helpful Extras
- [FIJI (FIJI Is Just ImageJ)](https://imagej.net/software/fiji/) is an excellent, open source software to view brain volumes quickly and easily.
  - [here](https://imagej.net/ij/docs/pdfs/ImageJ.pdf) is a great starter guide for all things ImageJ/FIJI
  - [here](https://www.youtube.com/watch?v=FiwjjbBjNy8) is a video showing a particularly usefl feature: if you have an aligned brain and a CCF or annotation volume, you can see them both in the same stack by following this tutorial. This is particularly useful for seeing probe tracks and identifying brain regions
  - many users find the segmented line tool particularly useful, or the [Fitline plugin](https://forum.image.sc/t/draw-a-best-fit-line-based-on-multi-point-selection/911)
- [BrainGlobe](https://brainglobe.info/index.html) has lots of great methods in python for these types of data. The PRA (Princeton Rat Atlas) is available in BrainGlobe, for example.