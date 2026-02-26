ANN_VOL="/groups/dennis/dennislab/dennise/github/cleared_brains/data/annotation_template_25_resliced.tif"
ANN_CSV="/groups/dennis/dennislab/dennise/github/cleared_brains/data/allen_anns-and-labels.csv"
ANN_MASK="/groups/dennis/dennislab/dennise/github/cleared_brains/data/ann_mask.tif"
CCF_VOL="/groups/dennis/dennislab/dennise/github/cleared_brains/data/axial_allenCCF_25.tif"
BRAIN_VOL="/groups/dennis/dennislab/Imaging/raw_imaging_data/${1}/processed/bigstitcher/${1}_fused_12.tif"

bsub -n 1 -o "logs/superscript_${1}.txt" -J "super${1}" ./superscript_all.sh $ANN_VOL $ANN_CSV $ANN_MASK $CCF_VOL $BRAIN_VOL $1
