# cleared_brains

## Purpose
The goals of this repo are:
1. to build on PRA repo, which produced the 2024 Dennis et al manuscript
2. include new tools and documentation as environments/processes evolve
3. share with our collaborators and later the public as we produce manuscripts

## To use
1. Clone this repo
2. Generate the lightsheet environment
  - in the repo folder, `mamba env create -f environment.yaml` this will create an environment called clearedbrains

If you're not at Janelia, you'll need to 

At Janelia:
- log in to login1 or login2
- start an interactive node 
  bsub -Is -W 04:00 -n 1 /bin/bash
- install miniconda
https://hhmi.atlassian.net/wiki/spaces/AL/pages/156205218/Data+processing+with+Python+on+the+Janelia+Compute+Cluster?atlOrigin=eyJpIjoiMjQ3ZTVkMGZmOGMxNGE0ZDhkNDVjZDUxODJiMDMzYmQiLCJwIjoiY29uZmx1ZW5jZS1jaGF0cy1pbnQifQ 

https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

- add to path (change /path/to/your/directory)
export PATH="$PATH:/path/to/your/directory"
- mamba env create -f environment.yaml
- conda activate clearedbrains
- check path:
  which python
- it should say ~/miniforge3/envs/clearedbrains...


## Data
Even downsampled files are large, so we have deposited the main files can be found here:

- rat data from the Princeton Ratlas (PRA) manuscript can be found [here](https://figshare.com/articles/dataset/Princeton_RAtlas_PRA_/24207429)
- _Mus caroli_ files can be found [here](link)

## Acknowledgements
This code builds off of PRA, which built heavily off of BrainPipe from Tom Pisano, Zahra Dahanerawala, and Austin Hoag. It also benefitted greatly from Nick Del Grosso and BrainGlobe. Thanks also to Nishan Shettigar and Alison Comrie for suggestions to improve the code.

## Citations
- Our [PRA protocol](https://en.bio-protocol.org/en/bpdetail?id=4854&type=0 ) for whole, cleared rat brains and alignments
- [PRA](https://github.com/emilyjanedennis/PRA/)
- [BrainPipe](https://github.com/PrincetonUniversity/BrainPipe)
- [BrainRender](https://www.biorxiv.org/content/10.1101/2020.02.23.961748v2)
- [Pisano _et al_ 2022](https://www.sciencedirect.com/science/article/pii/S2666166722001691)

# Using raw lightsheet images to:

### 1. Make a stitched, whole-brain

### 2. Make an atlas

### 3. Put a brain in atlas space

### 4. Put a third-party atlas/annotation into your atlas space 


# Helpful extras
- [FIJI (FIJI Is Just ImageJ)](https://imagej.net/software/fiji/) is an excellent, open source software to view brain volumes quickly and easily.
  - [here](https://imagej.net/ij/docs/pdfs/ImageJ.pdf) is a great starter guide for all things ImageJ/FIJI
  - [here](https://www.youtube.com/watch?v=FiwjjbBjNy8) is a video showing a particularly usefl feature: if you have an aligned brain and a CCF or annotation volume, you can see them both in the same stack by following this tutorial. This is particularly useful for seeing probe tracks and identifying brain regions
  - many users find the segmented line tool particularly useful, or the [Fitline plugin](https://forum.image.sc/t/draw-a-best-fit-line-based-on-multi-point-selection/911)
- [BrainGlobe](https://brainglobe.info/index.html) has lots of great methods in python for these types of data. Our PRA (Princeton Rat Atlas) is available in BrainGlobe, for example.