import pandas as pd
import glob
import re

tissues = ["adipose", "gastroc", "hypo", "islet", "kidney", "liver"]
annotation_path = "Code/Annotation Files/new_annotations.csv"
annotation = pd.read_csv(annotation_path)

def create_allez(tissue):
    modules_path = "Code/Tissue Modules/" + tissue + "/Raw Modules"
    universe_path = "Code/MetaNetwork Files/"+ tissue + "/" + tissue + "_metanetwork_nqrank_filtered.csv"
    gene_map_path = "Code/MetaNetwork Files/" + tissue + "/" + tissue + "_ensembl_gene_map.tab"
    module_files = glob.glob(modules_path + "/*.csv")
    universe = pd.read_csv(universe_path)
    gene_map = pd.read_csv(gene_map_path, sep="\t")

    for filepath in module_files:
        module = pd.read_csv(filepath)
        name = re.split("[.\/]", filepath)[-2]
        gene_symbols = [gene_map[gene_map["Entry"] == ensembl_id]["Gene names"].values[0] for ensembl_id in module["Accession"]]
        df = pd.DataFrame(gene_symbols, columns=["Gene symbols"])
        df.to_csv("Code/Allez Files/" + tissue + "/" + name + ".csv", index=False)
    
    universe_gene_symbols = [gene_map[gene_map["Entry"] == ensembl_id]["Gene names"].values[0] for ensembl_id in universe["Accession"]]
    df = pd.DataFrame(universe_gene_symbols, columns=["Gene symbols"])
    df.to_csv("Code/Allez Files/" + tissue + "/universe.csv", index=False)

for tissue in tissues:
    create_allez(tissue)
