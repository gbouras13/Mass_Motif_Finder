#!/usr/bin/env python3

import pandas as pd

# function to read the csv
def read_csv_motif(csv):
    # sample	contig	position	motif	locus_tag	gene	product
    df = pd.read_csv(csv, delimiter= ',', index_col=False)
    return df


def summarise_sample(summary_list, count_out, gene_out, summary_all_out):
    # read into list       
    summaries = []
    l =summary_list

    for a in l:
        tmp_summary = read_csv_motif(a)
        # remove first row (from the file)
        # tmp_summary = tmp_summary.iloc[1: , :]
        summaries.append(tmp_summary)

    # make into combined dataframe
    total_summary_df = pd.concat(summaries,  ignore_index=True)

    # count each sample

    count_df = (total_summary_df.groupby(['sample'])
        .agg({'contig':'size'})
        .rename(columns={'contig':'Number_Motif_Hits'})
        .reset_index())

    count_df.to_csv(count_out, sep=",", index=False)

    # count each gene

    gene_df = (total_summary_df.groupby(['gene','product','Uniprot'])
        .agg({'contig':'size'})
        .rename(columns={'contig':'Number_Motif_Hits'})
        .reset_index())

    gene_df.to_csv(gene_out, sep=",", index=False)

    total_summary_df.to_csv(summary_all_out, sep=",", index=False)
        

summarise_sample(snakemake.input.csvs, snakemake.output.summary_counts, snakemake.output.gene_counts, snakemake.output.all_hits)




