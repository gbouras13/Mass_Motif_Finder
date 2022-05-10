rule summary:
    input:
        csvs = expand(os.path.join(RESULTS,"{sample}.csv"), sample = SAMPLES)
    output:
        summary_counts = os.path.join(SUMMARY,"summary_counts.csv"),
        gene_counts = os.path.join(SUMMARY,"gene_counts.csv"),
        all_hits = os.path.join(SUMMARY,"all_motif_hits.csv")
    conda:
        os.path.join('..', 'envs','scripts.yaml')
    threads:
        1
    resources:
        mem_mb=BigJobMem
    script:
        '../scripts/summary_counts.py'

# rule summarise_by_gene:
#     input:
#         csv = os.path.join(TMP,"{sample}.csv"),
#         gff = os.path.join(GFFS,"{sample}.gff")
#     output:
#         csv = os.path.join(RESULTS,"{sample}.csv")
#     conda:
#         os.path.join('..', 'envs','scripts.yaml')
#     threads:
#         1
#     resources:
#         mem_mb=BigJobMem
#     script:
#         '../scripts/gff_finder.py'


rule aggr_statistics:
    """Aggregate."""
    input:
        os.path.join(SUMMARY,"summary_counts.csv"),
        os.path.join(SUMMARY,"gene_counts.csv"),
        os.path.join(SUMMARY,"all_motif_hits.csv")
    output:
        os.path.join(FLAGS, "aggr_summary.txt")
    threads:
        1
    resources:
        mem_mb=BigJobMem
    shell:
        """
        touch {output[0]}
        """