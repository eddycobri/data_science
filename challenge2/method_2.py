import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import pickle
from collections import Counter
import community as com
import challenge2_skeleton as ch2
import method_1 as m1 

def method_2(attribute,alpha=0):
    prediction = {}
    partitions = com.best_partition(m1.G)
    print(partitions)

    if attribute == m1.employer :
        default_attr = "university of illinois at urbana-champaign"
    elif attribute == m1.college:
        default_attr = "university of illinois at urbana-champaign"
    elif attribute == m1.location :
        default_attr = "urbana-champaign illinois area"


    for node in m1.empty_nodes :
        prediction[node] = []
        tab_attr = []
        nb_att = 0
        nb_total = 0
        attr = default_attr
        for k,v in partitions.items() :
            if v == partitions[node] : #Si node et k sont dans la meme partition
                #Qu'il soit labeled ou pas on incremente nb_total
                #Du moment qu'il est dans la partition
                nb_total +=1
                if k in attribute:
                    for val in attribute[k] :
                        tab_attr.append(val)

        #tab_attr contient toutes les valeurs d'attributs dans de la clique
        best = tab_attr[0]
        maxx = 0
        for i in tab_attr :
            cpt = 0
            for j in tab_attr :
                if m1.compare_string(i,j) :
                    cpt +=1
            if cpt > maxx :
                maxx = cpt
                best = i
        if cpt > len(tab_attr)/2 :
            prediction[node].append(best)
        #else :
            #prediction[node].append(default_attr)
    return prediction
'''
        print(tab_attr)
nbr_college = [0 for c in range(0,len(m1.all_colleges))]  

for i in range(0,len(m1.all_colleges)) :
    for k,v in m1.college.items() :
        if m1.in_list(m1.all_colleges[i],v) :
            nbr_college[i] +=1

m = max(nbr_college)
for i in range(0,len(nbr_college)) :
    if nbr_college[i] == m :
        print(m1.all_colleges[i])

nbr_employer = [0 for c in range(0,len(m1.all_employers))]  

for i in range(0,len(m1.all_employers)) :
    for k,v in m1.employer.items() :
        if m1.in_list(m1.all_employers[i],v) :
            nbr_employer[i] +=1

m = max(nbr_employer)
for i in range(0,len(nbr_employer)) :
    if nbr_employer[i] == m :
        print(m1.all_employers[i])

nbr_location = [0 for c in range(0,len(m1.all_locations))]  

for i in range(0,len(m1.all_locations)) :
    for k,v in m1.location.items() :
        if m1.in_list(m1.all_locations[i],v) :
            nbr_location[i] +=1

m = max(nbr_location)
for i in range(0,len(nbr_location)) :
    if nbr_location[i] == m :
        print(m1.all_locations[i])'''

groundtruth_employer={}
with open('mediumEmployer.pickle', 'rb') as handle:
    groundtruth_employer = pickle.load(handle)
result_e=m1.evaluation_accuracy(groundtruth_employer,method_2(m1.employer))
groundtruth_college={}
with open('mediumCollege.pickle', 'rb') as handle:
    groundtruth_college = pickle.load(handle)
result_c=m1.evaluation_accuracy(groundtruth_college,method_2(m1.college))
groundtruth_location={}
with open('mediumLocation.pickle', 'rb') as handle:
    groundtruth_location = pickle.load(handle)
result_l=m1.evaluation_accuracy(groundtruth_location,method_2(m1.location))
print("College : ",result_c)
print("Employer : ",result_e)
print("Location : ",result_l)