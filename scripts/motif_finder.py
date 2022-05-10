from Bio.Seq import Seq
import Bio.motifs as motifs
from Bio import SeqIO
import pandas as pd


def get_motif(motif_seq, fasta_in, out_file):

	motif = motif_seq
	rev_motif = Seq(motif_seq).reverse_complement()
	instances = [Seq(motif)]
	instances_rev = [rev_motif]
	m = motifs.create(instances)
	m_rev = motifs.create(instances_rev)
	
	
	reads = list(SeqIO.parse(fasta_in, "fasta"))

	summary = []

	# go the fwd first
	for i in range(len(reads)):
		for pos, seq in m.instances.search(reads[i].seq):
			list = [(i+1),pos, seq ]
			summary.append(list)

	# then rev
	for i in range(len(reads)):
		for pos, seq in m_rev.instances.search(reads[i].seq):
			list = [(i+1),pos, seq ]
			summary.append(list)

    # make into combined dataframe
	summary_motif_df = pd.concat(summary,  ignore_index=True)
	summary_motif_df.to_csv(out_file, sep=",", index=False)


get_motif(snakemake.params.motif , snakemake.input.fasta, snakemake.output.csv)