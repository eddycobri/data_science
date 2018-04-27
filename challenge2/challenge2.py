import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import pickle
from collections import Counter
from networkx.algorithms import community as com
import community

# load the graph
G = nx.read_gexf("mediumLinkedin.gexf")
#print("Nb of users in our graph: %d" % len(G))

# load the profiles. 3 files for each type of attribute
# Some nodes in G have no attributes
# Some nodes may have 1 attribute 'location'
# Some nodes may have 1 or more 'colleges' or 'employers', so we
# use dictionaries to store the attributes
college={}
location={}
employer={}
# The dictionaries are loaded as dictionaries from the disk (see pickle in Python doc)
with open('mediumCollege_60percent_of_empty_profile.pickle', 'rb') as handle:
    college = pickle.load(handle)
with open('mediumLocation_60percent_of_empty_profile.pickle', 'rb') as handle:
    location = pickle.load(handle)
with open('mediumEmployer_60percent_of_empty_profile.pickle', 'rb') as handle:
    employer = pickle.load(handle)
#################################################
######       DATA PREPARATION             #######
#################################################

#List of colleges
all_colleges = []
for k,v in college.items() :
    for i in v :
        if not (i in all_colleges) :
            all_colleges.append(i)

print("########################### ALL COLLEGES IN THE WORLD ###########################")
cpte = 0
for i in all_colleges :
    cpte +=1
    print(cpte," => ",i)

#List of Location
all_locations = []
for k,v in location.items() :
    for i in v :
        if not (i in all_locations) :
            all_locations.append(i)

print("########################### ALL LOCATION IN THE WORLD ###########################")
cpte = 0
for i in all_locations :
    cpte +=1
    print(cpte," => ",i)

#List of Emloyer
all_employer = []
for k,v in employer.items() :
    for i in v :
        if not (i in all_employer) :
            all_employer.append(i)

print("########################### ALL EMPLOYER IN THE WORLD ###########################")
cpte = 0
for i in all_employer :
    cpte +=1
    print(cpte," => ",i)


'''
This function compare two long strings decomposing them into 'pertinent' words


'''
def compare_string(string_one,string_two):
    no_relevent_words = ["at","of","in","for","and"]
    match_enough = False

    tab_one = "-".join(string_one.split(" ")).split("-")
    tab_two = "-".join(string_two.split(" ")).split("-")
    while "" in tab_one :
        tab_one.remove("")
    while "" in tab_two :
        tab_two.remove("")

    if len(tab_one)<len(tab_two):
        for i in tab_one:
            if not i in no_relevent_words : #If i is relevent
                if i in tab_two :
                    match_enough = True
                else :
                    match_enough = False
                    break
        #After the 'for', 'match_enough' is True if all the relevent words was in the other  list
    else : #The same with the list swaped
        for i in tab_two:
            if not i in no_relevent_words : #If i is relevent
                if i in tab_one :
                    match_enough = True
                else :
                    match_enough = False
                    break
    return match_enough
'''
#Method 1
#Use homophily
list_3_clique = com.k_clique_communities(G,3)
print(list(list_3_clique))

def homophily_based_method(dic_attribute):
    for node in G.nodes():
        for voisin in G.neighbors(node) :
            print("something")

def get_empty(attribute):
    empty = []
    for node in G.nodes():
        if not (node in attribute):
            empty.append(node)
    return empty
'''
#partition = community.best_partition(G)
#print("####### Partition")
#print(partition)

#print("Nombre de personnes sans locations : ",len(get_empty(location)))
#print("Nombre de personnes sans employer : ",len(get_empty(employer)))
#print("Nombre de personnes sans college : ",len(get_empty(college)))

def find_complete_profile(g):
    list_to_return =[]
    for node in g.nodes():
        if (node in college) and (node in employer) and (node in location) :
            list_to_return.append(node)
    return list_to_return

def find_partly_profile(g):
    list_to_return = []
    complete = find_complete_profile(g)
    for node in g.nodes():
        if ((node in college) or (node in employer) or (node in location)):
            if not (node in complete) :
                list_to_return.append(node)
    return list_to_return

print("######## Tous les gars avec les profiles complets #########")
eux_tous = find_complete_profile(G)
print(eux_tous)
print("Ils sont ", len(eux_tous))
print("Soit : ",(len(eux_tous)/811)*100)
print("######## Tous les gars avec les profiles partiellement remplis #########")
truc = find_partly_profile(G)
print("Les autres qui ont un peu mais pas tout XD sont : ",(len(truc)/811)*100)


#Tableau NodeXLocation