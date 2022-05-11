from cmath import nan
import pandas as pd

# function to get the locus tag (between ID= and the first semi colon)
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def get_gff_gene(csv_in, gff_in, csv_out, sample):

# read in motif_df and get contig & position

    #csv_in = "/Users/a1667917/Documents/Keith/Phage_Motif/TMP/D1.csv"

    #colnames=['contig', 'position', 'motif']
    # no need for colnames, they are inferred
    motif_df = pd.read_csv(csv_in, delimiter= ',', index_col=False)
    contig = motif_df['contig']
    position = motif_df['position']


    # read in the gff df
    colnames=['contig', 'evidence', 'type', 'start', 'end', 'score', 'strand', 'n', 'description'] 
    try:
        gff_df = pd.read_csv(gff_in, delimiter= '\t', index_col=False, header=None, names=colnames)
    except pd.errors.EmptyDataError:
        print('gff is empty')

    # get only the rows off gff 
    types = ['CDS', 'tRNA', 'rRNA', 'tmRNA']
    gff_df = gff_df[gff_df['type'].isin(types)]

    # instantiate the locus tag gene and product columns
    motif_df['locus_tag'] = "Non-Coding"
    motif_df['gene'] = "Non-Coding"
    motif_df['product'] = "Non-Coding"
    motif_df['Uniprot'] = "Non-Coding"
    motif_df['sample'] = sample
    # https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
    cols = motif_df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    motif_df = motif_df[cols]

    # loop over every motif hit 
    for i in range(len(contig)):

        # index starts at 1 for the series
        con = contig[i]
        pos = float(position[i])
        # find the row that has the position and contig
        # selecting rows based on condition

        selected_row_df = gff_df.loc[(gff_df['start'] <= pos) & (gff_df['end'] >= pos) & (gff_df['contig'] == str(con) ) ]

        # if empty return nan to gene and description
        empty = False
        # if empty - non coding region
        if selected_row_df.empty:
            empty = True
            print("This position is in a non-coding region")

        if empty == False:
        # get is_name and locus_tage
            selected_row_df['locus_tag'] = selected_row_df['description'].apply(lambda x: find_between(x,"ID=", ";"  ) )
            selected_row_df['Gene_Name'] = selected_row_df['description'].apply(lambda x: find_between(x,"Name=", ";"  ) )
            selected_row_df['Uniprot'] = selected_row_df['description'].apply(lambda x: find_between(x,"UniProtKB:", ";"  ) )
            selected_row_df[['description','product']] = selected_row_df['description'].str.split('product=',expand=True)
            motif_df['locus_tag'].iloc[i] = selected_row_df['locus_tag'].iloc[0]
            motif_df['gene'].iloc[i] = selected_row_df['Gene_Name'].iloc[0]
            motif_df['product'].iloc[i] = selected_row_df['product'].iloc[0]
            if selected_row_df['Uniprot'].iloc[0] != "":
                motif_df['Uniprot'].iloc[i] = selected_row_df['Uniprot'].iloc[0]
            

    # # write to csv
    motif_df.to_csv(csv_out, sep=",", index=False)


get_gff_gene(snakemake.input.csv,snakemake.input.gff, snakemake.output.csv, snakemake.wildcards.sample)
