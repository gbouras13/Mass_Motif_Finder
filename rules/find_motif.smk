
rule find_motif:
    input:
        fasta = os.path.join(FASTAS,"{sample}.fasta")
    output:
        csv = os.path.join(TMP,"{sample}.csv")
    params:
        motif = MOTIF
    conda:
        os.path.join('..', 'envs','scripts.yaml')
    threads:
        1
    resources:
        mem_mb=BigJobMem
    script:
        '../scripts/motif_finder.py'

rule add_gene_from_gff:
    input:
        csv = os.path.join(TMP,"{sample}.csv"),
        gff = os.path.join(PROKKA,"{sample}","{sample}.gff")
    output:
        csv = os.path.join(RESULTS,"{sample}.csv")
    params:
        motif = MOTIF
    conda:
        os.path.join('..', 'envs','scripts.yaml')
    threads:
        1
    resources:
        mem_mb=BigJobMem
    script:
        '../scripts/gff_finder.py'


rule aggr_motif:
    """Aggregate."""
    input:
        expand(os.path.join(RESULTS,"{sample}.csv"), sample = SAMPLES),
    output:
        os.path.join(FLAGS, "aggr_motif.txt")
    threads:
        1
    resources:
        mem_mb=BigJobMem
    shell:
        """
        touch {output[0]}
        """