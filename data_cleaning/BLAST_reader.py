def no_hit_or_not_C57BL6J(info,range_list,log, query_title):
    """If no hit or not C57BL/6J, append `None` to range_list and append log to log.
    
    Returns
    -------
    boolean
        True if no hit found or not C57BL/6J
        False if good
    """
    if len(info)==0:
        range_list.append(None)
        log.append((query_title, info))
        return True
    elif 'C57BL/6J' not in info[0]['description'][0]['title']:
        range_list.append(None)
        log.append((query_title, info[0]))
        return True
    return False

def chrom_corner_case(chromosome):
    """helper method used in get_chrom() that prunes chrom num in corner cases
    """
    if chromosome.endswith(' unlocalized genomic contig'):
        chromosome = chromosome[:-len(' unlocalized genomic contig')]
    elif chromosome.endswith(' genomic contig'):
        chromosome = chromosome[:-len(' genomic contig')]
    elif chromosome.endswith(' genomic patch of type FIX'):
        chromosome = chromosome[:-len(' genomic patch of type FIX')]
    elif chromosome.endswith(' genomic patch of type NOVEL'):
        chromosome = chromosome[:-len(' genomic patch of type NOVEL')]
    elif chromosome.endswith(' genomic scaffold'):
        chromosome = chromosome[:-len(' genomic scaffold')]
    return chromosome

def get_chrom(info,range_list,log, query_title):
    """
    Returns
    -------
    False : boolean
        if not a normal chromosome nor MT
    
    'MT' : str
        if it's MT
    
    chromosome number : int
        if it's a normal chromosome
    """
    ind_chrom = info[0]['description'][0]['title'].find('chromosome')
    ind_mt = info[0]['description'][0]['title'].find('mitochondrion')
    if ind_chrom==-1 and ind_mt==-1: # no chromosome number and not a MT
        range_list.append(None)
        log.append((query_title, info[0]))
        return False
    elif ind_chrom>0 and ind_mt!=-1: # MT identified
        chromosome = "MT"
        idf+=1
        return 'MT'
    elif ind_chrom>0 and ind_mt==-1:
        l = info[0]['description'][0]['title'].find(',')
        chromosome = info[0]['description'][0]['title'][ind_chrom+11:l]
        return chrom_corner_case(chromosome)

def first_hit(info, chromosome, range_list, log, query_title, thresh):
    """ Checks if the first hit is good. If good, append range to range_list.
        Otherwise, append log to log.
    
    Parameters
    ----------
    thresh : int
        alignment length >= thresh are considered as good
    
    Returns
    -------
    True : boolean
        if the 1st hit is good
        
    False : boolean
        otherwise if the 1st hit is not good
    """
    if info[0]['hsps'][0]['align_len']>=thresh:
        start=info[0]['hsps'][0]['hit_from']
        end=info[0]['hsps'][0]['hit_to']
        if int(end)>int(start):
            # chrom num:a-b(sign)
            signed_range = (chromosome + ':' + str(start) + '-' + str(end), '+')
        else:
            signed_range = (chromosome + ':' + str(end) + '-' + str(start), '-')
        range_list.append(signed_range)
        return True
    else:
        range_list.append(None)
        log.append((query_title, info[0]))
        return False

# def combined_hit(info,chromosome, range_list, log, query_title, thresh):
#     sign=info[0]['hsps'][0]['hit_strand'] 
#     start_points=[hit['hit_from'] for hit in info[0]['hsps']]
#     end_points=[hit['hit_to'] for hit in info[0]['hsps']]
#     if sign=='Plus':
#         start=min(start_points)
#         end=max(end_points)
#         if end-start>=thresh and end-start<=62:
#             signed_range = (chromosome + ':' + str(start) + '-' + str(end), '+')
#             range_list.append(signed_range)
#             print(query_title, signed_range)
#             print('')
#             return
#     elif sign=='Minus':
#         start=min(end_points)
#         end=max(start_points)
#         if end-start>=thresh and end-start<=62:
#             signed_range = (chromosome + ':' + str(start) + '-' + str(end), '-')
#             range_list.append(signed_range)
#             print(query_title, signed_range)
#             print('')
#             return
#     range_list.append(None)
#     log.append((query_title, info[0]))

def json_to_ranges(file):
    """ Converts a BLAST .jason output file to 3 lists
    
    Parameters
    ----------
    file : str
        name of the .json file
    
    Returns
    -------
    id_list : list
        a list of `query_title`s
    
    range_list : list
        a list of ranges: each range is an ordered 2-tuple: (x:a-b, +/-), where a < b
        
    log : list
        a list of logs that show all 60-mers that couldn't be aligned satisfactorily
    """
    import json
    with open(file) as file:
        data = json.load(file)
    id_list=[] # list of query_title's
    range_list=[]
    log=[]
    for i in range(len(data['BlastOutput2'])):
        
        id_list.append(data['BlastOutput2'][i]['report']['results']['search']['query_title'])
        
        info = data['BlastOutput2'][i]['report']['results']['search']['hits']
        
        if no_hit_or_not_C57BL6J(info,range_list,log, id_list[-1]):
            continue

        chromosome = get_chrom(info,range_list,log, id_list[-1])
        
        if chromosome==False:
            continue
            
        if first_hit(info,chromosome,range_list, log, id_list[-1], 58):
            continue

    return id_list, range_list, log

def get_df(file_names):
    """ Arrange a list of files into a table. Prints out the number of problematic 60-mers.
    
    Parameters
    ----------
    file_names : list
        a list of .json file names
    
    Returns
    -------
    df : pandas.DataFrame
        a dataframe that looks like this:
        
            | GeneID | Chromosome |   Start   |    End    |         Range         | Sign
         --------------------------------------------------------------------------------
          0 | 497628 |     1      | 113891385 | 113891444 | 1:113891385-113891444 |  -   
          1 | 497629 |     3      | 107741291 | 107741349 | 3:107741291-107741349 |  -   
                                                  .
                                                  .
                                                  .
    """
    import re
    import pandas as pd
    identifier, ranges, log = json_to_ranges(file_names[0])
    for i in range(1, len(file_names)):
        ii, rr, ll = json_to_ranges(file_names[i])
        identifier.extend(ii)
        ranges.extend(rr)
        log.extend(ll)
    df = pd.DataFrame({'GeneID':identifier})
    df['Chromosome'] = [i[0].split(':')[0] if i!=None else None for i in ranges]
    df['Start'] = [re.split(':|-', i[0])[1] if i!=None else None for i in ranges]
    df['End'] = [re.split(':|-', i[0])[2] if i!=None else None for i in ranges]
    df['Range'] = [i[0] if i!=None else None for i in ranges]
    df['Sign'] = [i[1] if i!=None else None for i in ranges]
    print(f"{len(df)-df['Sign'].count()} out of {len(df)} or {1-df['Sign'].count()/len(df):.2%} of the 60-mers could not be aligned satisfactorily and thus their locations are left blank.")
    return df