# -*- coding: utf-8 -*-
"""
Created 2021-08-05
@author: ejdennis

"""

import pandas as pd
import numpy as np

def reformat(str_in):
    if isinstance(str_in,str):
        if str_in[-1]== ' ':
            str_in = str_in[:-1]
        str_in = str_in.replace(" ","_")
        str_in = str_in.replace("/","_")
        str_in = str_in.replace(",","")
        str_out = str_in.lower()

        str_out = str_out.replace("_left","")
        str_out = str_out.replace("_right","")
        str_out = str_out.replace("left","")
        str_out = str_out.replace("right","")
    else:
        print('{} is not a string'.format(str_in))
    return str_out

def replace_with_common_name(pd_in,syns):
    pd_out = pd_in.copy()
    for i in np.arange(0,len(pd_out.name)):
        lab = pd_out.name[i]
        if isinstance(lab,str):
            lab = reformat(lab)
            if (syns.name == lab).any():
                pd_out.name[i]=check_for_syn(lab,syns)
    return pd_out


def check_for_syn(name,syns):
    if name in list(syns.name):
        synonymns = syns[syns.name==name]['common_name']
    else:
        synonymns=[]
    return synonymns


    # get the parent name of a given name/volume
def get_parent_id_from_praid(labeledvolume,praid):
    parentid=list(labeledvolume.loc[labeledvolume.id == praid,'parent_id'])[0]
    return parentid

# get the hierarchy/family tree of a given name in a given volume
def get_hierarchy(labeledvolume,praid,maxlen):
    familytree = []
    parentid = get_parent_id_from_praid(labeledvolume,praid)
    # if parent isn't root, look for grandparent
    while parentid > 0:
        # add parent/grandparent... to tree
        familytree.append(parentid)
        # get grandparent/great grandparent...
        parentid=get_parent_id_from_praid(labeledvolume,parentid)
    familytree.reverse()
    print('family tree was {}'.format(familytree))
    if len(familytree) < 1:
        familytree=0
    return familytree

    # get all dissimilarity values for each overlapping set in two labeled volumes
def get_dissimilarity(Alab,Aval,Blab,Bval):
    nameA = get_name(Alab,Aval)
    print(nameA)
    familytreeA = get_hierarchy(Alab,nameA)
    nameB = get_name(Blab,Bval)
    print(nameB)
    familytreeB = get_hierarchy(Blab,nameB)
    if len(familytreeA) > len(familytreeB):
        # if family tree A longer than B
        diss = get_diss_value(familytreeA,familytreeB)
    elif len(familytreeB) > len(familytreeA):
        diss = get_diss_value(familytreeB,familytreeA)
    else:
        da = get_diss_value(familytreeA,familytreeB)
        db = get_diss_value(familytreeB,familytreeA)
        diss = min(da,db)
    return diss
