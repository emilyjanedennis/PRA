# PRA

## Purpose
The goals of this repo are:
1. Allow others to replicate our lightsheet manuscript
2. Allow non-Brody users to use and take advantage of these tools
3. Allow Brody lab members easy access to the tools developed and implemented on Priniceton's HPC spock

## To use
1. Generate the lightsheet environment
2. Activate the ClearMap2 git module

## Acknowledgements
This code builds heavily off of BrainPipe from Tom Pisano, Zahra Dahanderawala, and Austin Hoag. It also benefitted greatly from Nick Del Grosso and BrainGlobe.

## Citations
- BrainPipe
- BrainGlobe

# #######################
## Development Plan
1. Add code to recreate existiing figures -- as I add things, add any dependencies and make all paths relative
2. make a princeton users specific set of instructions



**THOUGHTS --> turn into todos**   
- really thinking about starting a fresh repo and 'doing things right'

- ideal to do the inj site on already transformed brains in space as downsizing isn't an issue with these areas. to do this, I want to add a step where we use transformix on the cell_in_atl volume to bring it into PRA space. once that's done I need to get all cell, reg volumes from their respective folders and put them all in a common format (brainname_channel_in_atl.tif) in one folder and then use this for analysis.

- I also want to add a cm2 output -- take a few 20 slice projections (avg over 20 slices) and overlay the cell centers before and after filters. -- ideally maybe do 20 slices near the front/middle of the brain coronally, 20 slices axially, and 20 slices sagittally. Feels like that should ~always get what people need.

- Also want to add a cleanup check -- after full script is run, see if all the important bits are there for each brain/ch. If not, flag -- if I do this in python using pandas and adding a csv file with brain // channel // stage 1 or 0 (basically a kanban board) would be awesome. Could output this from each script and then concatenate at the end -- would allow us to also have the slurm id which can be helpful in finding relevant logs.

- For inj centers -- plot points in axial x/y and saggital x/y on PRA and spit out. do for each brain and for all brains.
