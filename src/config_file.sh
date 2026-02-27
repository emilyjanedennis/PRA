# configuration variables

# point to your conda/mamba environment
ENV_PATH="/groups/dennis/home/dennise/miniforge3/envs/cm2/bin/python"
CLEARED_BRAINS_FLD="/groups/dennis/dennislab/dennise/github/cleared_brains"

# if not using ClearMap steps, can comment these lines out
CM2_SCRIPTS_PATH="/groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts"
cp CellMapFiles/* $CM2_SCRIPTS_PATH

# if not using BigStitcher steps, can comment out rest of file
BIG_STITCHER_PATH="/groups/dennis/dennislab/dennise/github/BigStitcher-Spark"
# path to your JAVA
export JAVA_HOME=/misc/sc/jdks/8.0.275.fx-zulu
# add apache-maven bin and JAVA bin to path, necessary for BigStitcher-Spark to work
export PATH=$PATH:/groups/dennis/dennislab/dennise/github/apache-maven-3.9.9/bin
export PATH=$JAVA_HOME/bin:$PATH