import vcf
import tabix 
import pandas as pd
import numpy as np
import re
from pyensembl import EnsemblRelease

snps_path = "Code/Annotation Files/BTBR_T__Itpr3tf_J.mgp.v5.snps.dbSNP142.vcf.gz"
indels_path = "Code/Annotation Files/BTBR_T__Itpr3tf_J.mgp.v5.indels.dbSNP142.normed.vcf.gz"
sv_insertions_path = "Code/Annotation Files/mgpv5.SV_insertions.bed.gz"
sv_deletions_path = "Code/Annotation Files/mgpv5.SV_deletions.bed.gz"
annotations_path = "Code/Annotation Files/annotation.csv"
ranges_path = "Code/Annotation Files/ranges.csv"
entrez_path = "Code/Annotation Files/entrez.csv"

snps_reader = vcf.Reader(filename=snps_path)
indels_reader = vcf.Reader(filename=indels_path)
sv_insertions_tb = tabix.open(sv_insertions_path)
sv_deletions_tb = tabix.open(sv_deletions_path)
annotations = pd.read_csv(annotations_path)
ranges = pd.read_csv(ranges_path)                                                                                                                                                                         
ensembl = EnsemblRelease(102, species="mouse")  
entrez = pd.read_csv(entrez_path)

accession_to_id_dict = pd.Series(annotations["a_substance_id"].values, index=annotations["a_gene_id"]).to_dict()

def find_snps(chromosome, start, end):
    """ Finds all the snps in a given range
    @param chromosome - target chromosome
    @param start - starting base pair
    @param end - ending base pair
    @return list of all snps in the range
    """
    global snps_reader
    return [
        {
            "Chromosome": record.CHROM,
            "POS": record.POS,
            "REF": record.REF,
            "ALT": record.ALT
        } for record in snps_reader.fetch(str(chromosome), start, end)
    ]

def find_indels(chromosome, start, end):
    """ Finds all the indels in a given range
    @param chromosome - target chromosome
    @param start - starting base pair
    @param end - ending base pair
    @return list of all indels in the range
    """
    global indels_reader
    return [
        {
            "Chromosome": record.CHROM,
            "POS": record.POS,
            "REF": record.REF,
            "ALT": record.ALT
        } for record in indels_reader.fetch(str(chromosome), start, end)
    ]

def find_sv_insertions(range):
    """ Finds all the sv insertions in a given range
    @param range - range of search in the form chromosome:start-end
    @return list of all sv insertions in the range
    """
    global sv_insertions_tb
    sv_insertions = []
    for record in sv_insertions_tb.querys(cur["Range"]):
        BTBR_data = record[11].split(";")  # 11 is hardcoded as the column with BTBR data
        if BTBR_data[0] != ".":
            sv_insertions.append({
                "POS": BTBR_data[0]
            })    
    return sv_insertions

def find_sv_deletions(range):
    """ Finds all the sv deletions in a given range
    @param range - range of search in the form chromosome:start-end
    @return list of all sv deletions in the range
    """
    global sv_deletions_tb
    sv_deletions = []
    for record in sv_deletions_tb.querys(cur["Range"]):
        BTBR_data = record[11].split(";")  # 11 is hardcoded as the column with BTBR data
        if BTBR_data[0] != ".":
            sv_deletions.append({
                "POS": BTBR_data[0]
            })    
    return sv_deletions

variants = pd.DataFrame(columns=["a_substance_id", "GeneSymbol", "EnsemblGeneId", "EntrezGeneId", "NearestGeneOffset", "Valid", "Snps", "Indels", "SV_Insertions", "SV_Deletions"]) 

# find all snps indels svs in the probe sequences
for i in range(ranges.shape[0]):
    cur = ranges.iloc[i]
    if i % 5000 == 0:
        print(i, "/", ranges.shape[0])  # progress tracker
    d = {
            "Snps": [],
            "Indels": [],
            "SV_Insertions": [],
            "SV_Deletions": [],
            "Valid": False,
            "a_substance_id": np.NaN,
            "GeneSymbol": np.NaN,
            "EnsemblGeneId": np.NaN,
            "EntrezGeneId": np.NaN,
            "NearestGeneOffset": np.NaN
        }                                                                                                                                                                                                     
    if not pd.isnull(cur["Range"]): # check if probe has a valid range
        if cur["Chromosome"] != "MT": # ignore mitochondrial probe hits                        
            # record all snps
            d["Snps"] = find_snps(cur["Chromosome"], cur["Start"], cur["End"]) 
            # record all indels
            d["Indels"] = find_indels(cur["Chromosome"], cur["Start"], cur["End"])        
            # record all sv insertions
            d["SV_Insertions"] = find_sv_insertions(cur["Range"])
            # record all sv deletions
            d["SV_Deletions"] = find_sv_deletions(cur["Range"])

        # find the gene symbol corresponding to this probe             
        offset = 0
        genes = ensembl.genes_at_locus(contig=cur["Chromosome"], position=int(cur["Start"]) - offset, end=int(cur["End"]) + offset, strand=cur["Sign"]) 

        while len(genes) == 0:
            offset += 100
            genes = ensembl.genes_at_locus(contig=cur["Chromosome"], position=int(cur["Start"]) - offset, end=int(cur["End"]) + offset, strand=cur["Sign"]) 

        d["GeneSymbol"] = genes[0].gene_name 
        d["EnsemblGeneId"] = genes[0].gene_id
        entrez_gene_ids = entrez[entrez["ensembl_gene_id"] == d["EnsemblGeneId"]]["entrezgene_id"].values
        if len(entrez_gene_ids) > 0:
            d["EntrezGeneId"] = entrez_gene_ids[0]
        d["NearestGeneOffset"] = offset     

    # mark if probe is valid
    if not pd.isnull(cur["Range"]) and len(d["Snps"]) == 0 and len(d["Indels"]) == 0 and len(d["SV_Insertions"]) == 0 and len(d["SV_Deletions"]) == 0:                                                        
        d["Valid"] = True
    else:
        d["Valid"] = False                             

    # find a_substance_id using gene transcript id
    d["a_substance_id"] = accession_to_id_dict.get(cur["GeneID"], np.NaN)
    variants = variants.append(d, ignore_index=True)

### create final annotation df and output it
final_df = pd.concat([ranges, variants], axis=1)
final_df.Valid = final_df.Valid == 1
final_df.rename(columns={"GeneID": "TranscriptID"}, inplace=True)
final_df.to_csv("Code/Annotation Files/new_annotations.csv", index=False)
