#!/bin/env bash
#

#SBATCH -c 1                      # number of cores
#SBATCH -t 20                  # time (minutes)
#SBATCH -o logs/clearmap2_%j.out        # STDOUT #add _%a to see each array job
#SBATCH -e logs/clearmap2_%j.err        # STDERR #add _%a to see each array job

cat /proc/$$/status | grep Cpus_allowed_list
module load anacondapy/2020.11
. activate cm2

# change these:
declare -a LIST_OF_FOLDERS=("/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco-E155/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RES(10565x7620x3837)/046480/046480_088370/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco-E155/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RES(10564x7615x3832)/046480/046480_088390/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_M122/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RES(10550x7618x2302)/046110/046110_101740/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_M122/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RES(10544x7602x2335)/046240/046240_101960/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_X077/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RES(10582x7586x4069)/045600/045600_096560/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_X077/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RES(10543x7615x4132)/046290/046290_096450/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_X078/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RES(10565x7620x3837)/046480/046480_088370/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_X078/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RES(10564x7615x3832)/046480/046480_088390/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_E130/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RES(10567x7590x3472)/071300/071300_096970/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_E130/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RES(10553x7594x3511)/071280/071280_096920/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_E154/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RESx10563x7615x3459/071300/071300_090420/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_E154/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RESx10555x7589x3547/071300/071300_091050/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_E156/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_E156/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_M128/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RES(10492x7613x3710)/076490/076490_094830/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488/pb_udisco_647_488_M128/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RES(10590x7592x3785)/076490/076490_095390/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_/pb_udisco_647_488_E131/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_/pb_udisco_647_488_E131/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RESx12060x7605x3756/058950/058950_093200/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_/pb_udisco_647_488_A296/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_/pb_udisco_647_488_A296/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RESx10557x7600x3485/091390/091390_095610/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_/pb_udisco_647_488_A300/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_/pb_udisco_647_488_A300/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RESx12060x7605x3756/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-009/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-009/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-008/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-008/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-007/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-007/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-006/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-006/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-005/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-005/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-004/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-004/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-003/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-003/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-002/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-002/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-001/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/"
                        "/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco_647_488_4x/pb_udisco_647_488_4x-001/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_X073/imaging_request_1/rawdata/resolution_3.6x/Ex_488_Em_0_corrected/RES(10519x7581x4124)/082890/082890_087410/"
			"/jukebox/LightSheetData/lightserv/pbibawi/pb_udisco/pb_udisco_X073/imaging_request_1/rawdata/resolution_3.6x/Ex_642_Em_2_corrected/RES(10516x7619x4092)/082910/082910_087140/")

declare -a LIST_OF_DESTINATIONS=(
				"/scratch/ejdennis/cm2_brains/E155/488"
				"/scratch/ejdennis/cm2_brains/E155/642"
                                "/scratch/ejdennis/cm2_brains/M122/488"
                                "/scratch/ejdennis/cm2_brains/M122/642"
                                "/scratch/ejdennis/cm2_brains/X077/488"
                                "/scratch/ejdennis/cm2_brains/X077/642"
                                "/scratch/ejdennis/cm2_brains/X078/488"
                                "/scratch/ejdennis/cm2_brains/X078/642"
                                "/scratch/ejdennis/cm2_brains/E130/488"
                                "/scratch/ejdennis/cm2_brains/E130/642"
                                "/scratch/ejdennis/cm2_brains/e154/488"
                                "/scratch/ejdennis/cm2_brains/e154/642"
                                "/scratch/ejdennis/cm2_brains/e156/488"
                                "/scratch/ejdennis/cm2_brains/e156/642"
                                "/scratch/ejdennis/cm2_brains/m128/488"
                                "/scratch/ejdennis/cm2_brains/m128/642"
                                "/scratch/ejdennis/cm2_brains/E131/488"
                                "/scratch/ejdennis/cm2_brains/E131/642"
                                "/scratch/ejdennis/cm2_brains/A296/488"
                                "/scratch/ejdennis/cm2_brains/A296/642"
                                "/scratch/ejdennis/cm2_brains/A300/488"
                                "/scratch/ejdennis/cm2_brains/A300/642"
                                "/scratch/ejdennis/cm2_brains/e144/488"
                                "/scratch/ejdennis/cm2_brains/e144/642"
                                "/scratch/ejdennis/cm2_brains/e143/488"
                                "/scratch/ejdennis/cm2_brains/e143/642"
                                "/scratch/ejdennis/cm2_brains/a253/488"
                                "/scratch/ejdennis/cm2_brains/a253/642"
                                "/scratch/ejdennis/cm2_brains/j319/488"
                                "/scratch/ejdennis/cm2_brains/j319/642"
                                "/scratch/ejdennis/cm2_brains/h234/488"
                                "/scratch/ejdennis/cm2_brains/h234/642"
                                "/scratch/ejdennis/cm2_brains/e142/488"
                                "/scratch/ejdennis/cm2_brains/e142/642"
                                "/scratch/ejdennis/cm2_brains/e153/488"
                                "/scratch/ejdennis/cm2_brains/e153/642"
                                "/scratch/ejdennis/cm2_brains/j316/488"
                                "/scratch/ejdennis/cm2_brains/j316/642"
                                "/scratch/ejdennis/cm2_brains/j317/488"
                                "/scratch/ejdennis/cm2_brains/j317/642"
				"/scratch/ejdennis/cm2_brains/X073/488"
				"/scratch/ejdennis/cm2_brains/X073/642")

module load anacondapy/2020.11
. activate cm2

for (( n=0; n<=${#LIST_OF_FOLDERS[@]}; n++ ))
do
    echo "$n"    
    echo "${LIST_OF_FOLDERS[n]}"
    echo "${LIST_OF_DESTINATIONS[n]}"
    OUT0=$(sbatch --array=0 -p Brody cm2_prep.sh "${LIST_OF_FOLDERS[n]}" "${LIST_OF_DESTINATIONS[n]}" "smartspim")
    echo "$OUT0"
    sbatch --dependency=afterany:${OUT0##* } -p Brody --array=0 cm2_process.sh "${LIST_OF_FOLDERS[n]}" "${LIST_OF_DESTINATIONS[n]}" "smartspim"
done






