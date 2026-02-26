# configuration variables

# point to your conda/mamba environment
ENV_PATH="/groups/dennis/home/dennise/miniforge3/envs/cm2/bin/python"
CLEARED_BRAINS_FLD="/groups/dennis/dennislab/dennise/github/cleared_brains"

# if using ClearMap steps
CM2_SCRIPTS_PATH="/groups/dennis/dennislab/dennise/github/ClearMap2/ClearMap/Scripts"

# if using BigStitcher steps
BIG_STITCHER_PATH="/groups/dennis/dennislab/dennise/github/BigStitcher-Spark"

# set up for BigStitcher-Spark
export JAVA_HOME=/misc/sc/jdks/8.0.275.fx-zulu
export PATH=$PATH:/groups/dennis/dennislab/dennise/github/apache-maven-3.9.9/bin
export PATH=$JAVA_HOME/bin:$PATH