source ./config_file.sh

# you need to update "BRAIN_VOL's path" to adjust
ANN_VOL="${CLEARED_BRAINS_FLD}/data/annotation_template_25_resliced.tif"
ANN_CSV="${CLEARED_BRAINS_FLD}/data/allen_anns-and-labels.csv"
ANN_MASK="${CLEARED_BRAINS_FLD}/data/ann_mask.tif"
CCF_VOL="${CLEARED_BRAINS_FLD}/data/axial_allenCCF_25.tif"
BRAIN_VOL="/groups/dennis/dennislab/Imaging/raw_imaging_data/${1}/processed/bigstitcher/${1}_fused_12.tif"

bsub -n 1 -o "logs/superscript_${1}.txt" -J "super${1}" ./example_superscript_all.sh $ANN_VOL $ANN_CSV $ANN_MASK $CCF_VOL $BRAIN_VOL $1
