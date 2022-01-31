import pandas as pd
import re

uncleaned_data_filenames = ["Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/adipose_int2_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/gastroc_int2_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/hypo_int2_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/islet_int2_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/kidney_int2_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/liver_int2_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/adipose_mlratio_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/gastroc_mlratio_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/hypo_mlratio_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/islet_mlratio_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/kidney_mlratio_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/liver_mlratio_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/adipose_mlratio_nqrank_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/gastroc_mlratio_nqrank_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/hypo_mlratio_nqrank_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/islet_mlratio_nqrank_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/kidney_mlratio_nqrank_final.csv",
                            "Data sets for F2 mice/mlratio and intensity2 for F2 mice/CSV/liver_mlratio_nqrank_final.csv"]   

filtering_path = "Code/Annotation Files/new_annotations.csv"

def import_data(filename):
    data = pd.read_csv(filename, index_col=0).transpose()
    data.index.name = "TranscriptID"
    print("reading", filename)
    return data    

data_dfs = [import_data(filename) for filename in uncleaned_data_filenames]
filtering_df = pd.read_csv(filtering_path)
valid_gene_ids = set([filtering_df.iloc[i].TranscriptID for i in range(filtering_df.shape[0]) if filtering_df.iloc[i].Valid])

def filter_valid(row):
    return int(row.name) in valid_gene_ids

final_data_dfs = [data[data.apply(filter_valid, axis=1)].transpose() for data in data_dfs]                                                                                                                      
for i in range(len(final_data_dfs)):               
    new_filename = re.split("[.\/]", uncleaned_data_filenames[i])[-2] + "_cleaned.csv"
    print("writing", new_filename)
    final_data_dfs[i].to_csv("Data sets for F2 mice/mlratio and intensity2 for F2 mice/Cleaned CSVs/" + new_filename)      
