### Data Cleaning Scripts

- blast_reader.py: reads json files from BLAST results
- gen_annotation.py: creates revised annotation file from the parsed blast results (finds clean transcripts)
- clean_datasets.py: cleans datasets using the new annotation
- gen_modules.py: creates transcript->module mapping using WGCNA results
- gen_allez.py: creates allez input using modules
- find_pathways.py: finds significantly enriched modules and corresponding pathways using allez results
