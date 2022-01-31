import pandas as pd
import glob
import re

tissues = ["adipose", "gastroc", "hypo", "islet", "kidney", "liver"]
annotation_path = "Code/Annotation Files/new_annotations.csv"
annotation = pd.read_csv(annotation_path)

def make_modules(tissue):
    modules_path = "Code/Tissue Modules/" + tissue + "/Raw Modules"
    module_files = glob.glob(modules_path + "/*.csv")
    
    ensembl_dict = {}
    transcript_id_dict = {}
    for filepath in module_files:
        module = pd.read_csv(filepath)
        name = re.split("[.\/]", filepath)[-2]
        transcript_ids = annotation[annotation["EnsemblGeneId"].isin(module["Accession"])]["TranscriptID"].tolist()
        for ensembl_id in module["Accession"]:
            ensembl_dict[ensembl_id] = [name]
        for transcript_id in transcript_ids:
            transcript_id_dict[transcript_id] = [name]

    ensembl_df = pd.DataFrame(ensembl_dict).transpose()
    transcript_id_df = pd.DataFrame(transcript_id_dict).transpose()
    ensembl_df.index.name = "EnsemblGeneId"
    ensembl_df.columns = ["ModuleColor"]
    transcript_id_df.index.name = "TranscriptID"
    transcript_id_df.columns = ["ModuleColor"]

    output_path = "Code/Tissue Modules/" + tissue
    ensembl_df.to_csv(output_path + "/ensembl_map.csv")
    transcript_id_df.to_csv(output_path + "/transcript_id_map.csv")

for tissue in tissues:
    make_modules(tissue)
