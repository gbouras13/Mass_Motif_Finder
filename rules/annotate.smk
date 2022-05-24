rule prokka:
    """Run prokka."""
    input:
        os.path.join(FASTAS,"{sample}.fasta")
    output:
        os.path.join(PROKKA,"{sample}","{sample}.gff")
    params:
        os.path.join(PROKKA, "{sample}")
    conda:
        os.path.join('..', 'envs','prokka.yaml')
    threads:
        BigJobCpu
    resources:
        mem_mb=BigJobMem
    shell:
        'prokka --outdir {params[0]}  --prefix {wildcards.sample} {input[0]} --force'





