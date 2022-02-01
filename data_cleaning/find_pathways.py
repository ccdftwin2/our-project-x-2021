import pandas as pd
import glob
import re
from collections import defaultdict
from goatools import obo_parser
import wget
import os

go_obo_url = "http://geneontology.org/ontology/go-basic.obo"
data_folder = os.getcwd()
# Check if we have the ./data directory already
if(not os.path.isfile(data_folder)):
    # Emulate mkdir -p (no error if folder exists)
    try:
        os.mkdir(data_folder)
    except OSError as e:
        if(e.errno != 17):
            raise e
else:
    raise Exception('Data path (' + data_folder + ') exists as a file. '
                   'Please rename, remove or change the desired location of the data path.')

# Check if the file exists already
if(not os.path.isfile(data_folder+'/go-basic.obo')):
    go_obo = wget.download(go_obo_url, data_folder+'/go-basic.obo')
else:
    go_obo = data_folder+'/go-basic.obo'

go = obo_parser.GODag(go_obo)

def find_pathways(tissue):
    modules_path = "Code/Tissue Modules/" + tissue + "/Raw Modules"
    pathways_path = "Code/Allez Results/" + tissue
    out_path = "Code/Allez Results/Pathways"
    module_names = [re.split("[.\/]", filepath)[-2] for filepath in glob.glob(modules_path + "/*.csv")]

    df_dict = {"Module Color": [], "Pathway": [], "Z-score": [], "Num Overlap": [], "Namespace": [], "Significant": []}
    for module in module_names:
        pathway = pd.read_csv(pathways_path + "/" + module + "_enrichment_allsets_sig.txt", sep="\t").sort_values(by="z.score", ascending=False)
        df_dict["Module Color"].append(module)
        sig_pathway = False
        for i in range(pathway.shape[0]):
            cur = pathway.iloc[i]
            if cur["z.score"] >= 5 and cur["num.overlap"] > 5 and go[cur["GO_ID"]].namespace == "biological_process":
                df_dict["Pathway"].append(cur["Term"])
                df_dict["Z-score"].append(cur["z.score"])
                df_dict["Num Overlap"].append(cur["num.overlap"])
                df_dict["Namespace"].append(go[cur["GO_ID"]].namespace)
                df_dict["Significant"].append(True)
                sig_pathway = True
                break
        
        if not sig_pathway:
            df_dict["Pathway"].append(pathway.iloc[0]["Term"])
            df_dict["Z-score"].append(pathway.iloc[0]["z.score"])
            df_dict["Num Overlap"].append(pathway.iloc[0]["num.overlap"])
            df_dict["Namespace"].append(go[pathway.iloc[0]["GO_ID"]].namespace)
            df_dict["Significant"].append(False)
    df = pd.DataFrame(df_dict)
    df.to_csv(out_path  + "/" + tissue + "_pathways.csv", index=False)
    print("Wrote " + tissue)

tissues = ["adipose", "gastroc", "hypo", "islet", "kidney", "liver"]
for tissue in tissues:
    find_pathways(tissue)
