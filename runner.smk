"""
The snakefile that runs the pipeline.
Manual launch example:


 snakemake -c 1 -s runner.smk --use-conda --config Fastas='/hpcfs/users/a1667917/s_aureus/e_coli_fasta' \
 Output=/hpcfs/users/a1667917/s_aureus/e_coli_motif Motif='AGCGCAAGTA' --conda-frontend conda 

 snakemake -c 1 -s runner.smk --use-conda --config Fastas='/Users/a1667917/Documents/Total_Staph/final_fastas' \
 Output=/Users/a1667917/Documents/Keith/Phage_Motif Motif='AGCGCAAGTA'  --conda-create-envs-only --conda-frontend conda 


"""

import os

### config
# 16 GB
BigJobMem=16000
# 16 threads
BigJobCpu=16

# no need for memory etc
### DIRECTORIES

include: "rules/directories.smk"

# get if needed
OUTPUT = config['Output']
FASTAS = config["Fastas"]
#GFFS = config["Gffs"]
MOTIF = config["Motif"]
# samples
include: "rules/samples.smk"
sampleFastas = samplesFromDirectory(FASTAS)
SAMPLES = sampleFastas.keys()
#print(SAMPLES)


# Import rules and functions
include: "rules/targets.smk"
include: "rules/annotate.smk"
include: "rules/find_motif.smk"
include: "rules/summarise.smk"

rule all:
    input:
        TargetFiles
