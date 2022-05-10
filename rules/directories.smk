"""
Database and output locations for Hecatomb
Ensures consistent variable names and file locations for the pipeline.
"""


### OUTPUT DIRECTORY
if config['Output'] is None:
    OUTPUT = 'Motifs_Output'
else:
    OUTPUT = config['Output']


### OUTPUT DIRs
FLAGS = os.path.join(OUTPUT, 'FLAGS')
RESULTS = os.path.join(OUTPUT, 'RESULTS')
SUMMARY = os.path.join(OUTPUT, 'SUMMARY')







