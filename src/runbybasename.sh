ARG1="/groups/dennis/dennislab/dennise/github/cleared_brains/data/annotation_template_25_resliced.tif"
ARG2="/groups/dennis/dennislab/dennise/github/cleared_brains/data/allen_anns-and-labels.csv"
ARG3="/groups/dennis/dennislab/dennise/github/cleared_brains/data/ann_mask.tif"
ARG4="/groups/dennis/dennislab/dennise/github/cleared_brains/data/axial_allenCCF_25.tif"
ARG5="/groups/dennis/dennislab/Imaging/raw_imaging_data/${1}/processed/bigstitcher/${1}_fused_12.tif"
ARG6=${1}
bsub -n 1 -o "logs/superscript_${1}.txt" -J "super${1}" ./superscript_all.sh $ARG1 $ARG2 $ARG3 $ARG4 $ARG5 $ARG6
