import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import pickle
from collections import Counter
import challenge2_skeleton as ch2

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

print("Nb of users with one or more attribute college: %d" % len(college))
print("Nb of users with one or more attribute location: %d" % len(location))
print("Nb of users with one or more attribute employer: %d" % len(employer))

# here are the empty nodes for whom your challenge is to find the profiles
empty_nodes=[]
with open('mediumRemovedNodes_60percent_of_empty_profile.pickle', 'rb') as handle:
    empty_nodes = pickle.load(handle)
#print(empty_nodes)

G = nx.read_gexf("mediumLinkedin.gexf")

pred_employer = {}
pred_college = {}
pred_location = {}
def compare_string(string_one,string_two):
    no_relevent_words = ["new","at","of","in","for","and","area","state","city","town","university","college","office","department","laboratory"]
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

def in_list(string,mList):
    for i in mList :
        if compare_string(string,i) :
            return True
    return False

#Initialisation des dictionnaires de prediction
for node in empty_nodes:
    pred_employer[node] = []
    pred_college[node] = []
    pred_location[node] = []

all_locations = []
for k,v in location.items() :
    for i in v :
        if not in_list(i,all_locations) :
            all_locations.append(i)
all_colleges = []
for k,v in college.items() :
    for i in v :
        if not in_list(i,all_colleges) :
            all_colleges.append(i)
all_employers = []
for k,v in employer.items() :
    for i in v :
        if not in_list(i,all_employers) :
            all_employers.append(i)
'''
Renvoie True si l'attribut name se trouve dans la location loc
ie: Si on retrouve le nom de la location dans le nom de name

'''
def name_in_location(loc,name):
    no_relevent_words = ["new","at","of","in","for","and","area","state","city","town","university","college","office","department","laboratory"]
    loc = loc.lower()
    name = name.lower()
    loc = loc.split()
    for i in loc :
        if not i in no_relevent_words:
            if i in name :
                return True
    return False
'''
    Cette fonction prends en parametre la valeur d'un employer et d'un college et
    renvoie un ratio qui le nombre de noeuds ayant les deux attributs par le nombre 
    de noeuds ayant juste cette valeur d'employer

    La valeur retournee reflete a quel point les gens ayant l'attribut emp sont succeptibles
    d'avoir l'attribut col
'''
def corr_emp_col(emp,col): # emp => col
    nodes_with_emp = 0
    nodes_with_both = 0
    for node, val_emp in employer.items() :
        if emp in val_emp : #Si le noeud a l'attribut employer on doit check s'il a l'attribut col
            nodes_with_emp +=1
            if node in college:
                if col in college[node]: #Si le noeud a aussi l'attribut college
                    nodes_with_both +=1
    if nodes_with_emp == 0 :
        return 0
    else :
        return nodes_with_both/nodes_with_emp
def corr_col_emp(col,emp): # col => emp
    nodes_with_col = 0
    nodes_with_both = 0
    for node, val_col in college.items() :
        if col in val_col : #Si le noeud a l'attribut employer on doit check s'il a l'attribut col
            nodes_with_col +=1
            if node in employer:
                if col in employer[node]: #Si le noeud a aussi l'attribut college
                    nodes_with_both +=1
    if nodes_with_col == 0 :
        return 0
    else :
        return nodes_with_both/nodes_with_col
'''
Prend en parametre une location et un attribut (en string. Ex : "employer") et renvoie un liste de toutes les
valeur de l'attributs dans cette location
'''
def attr_in_location(loc,attribute):
    global all_employers
    global all_employers
    global all_locations
    list_to_return = []
    if attribute == "employer":
        for emp in all_employers:
            if name_in_location(loc,emp):
                list_to_return.append(emp)
    elif attribute == "college" :
        for col in all_colleges :
            if name_in_location(loc,col):
                list_to_return.append(col)
    return list_to_return
'''  
def end_inference():
    global pred_college
    global pred_employer
    global pred_location
    global empty_nodes

    end = True

    for node in empty_nodes:
        if len(pred_college[node])<1 or len(pred_employer[node])<1 or len(pred_location[node])<1 :
            end = False
            break
    return end

def inference():

    global pred_college
    global pred_employer
    global pred_location

    global empty_nodes

    global all_colleges
    global all_employers
    global all_locations

    global college
    global employer
    global location
    
    while not end_inference() :
        print("Boucle!")
        for node in empty_nodes:
            nbrs_attr_values=[]
            for voisin1 in G.neighbors(node):
                
                
                    Cette partie complete les profiles en considerant que un triade 
                    partage toujours un attribut (Ce qui n'est pas toujours vrai) mais très probable

                for voisin2 in G.neighbors(node):
                    
                    if voisin1 != voisin2 :
                        if voisin1 in G.neighbors(voisin2) :
                            #Si voisin1 et voisin2 sont aussi voisins
                            #ie. On a eu triade
                            #On check si ces derniers ont un attribut en commun
                            if voisin1 in location :
                                if voisin2 in location:
                                    for i in location[voisin1] :
                                        if i in location[voisin2] :
                                            #On peut dire que node a l'attribut i
                                            if not i in pred_location[node]:
                                                pred_location[node].append(i)
                                elif voisin2 in pred_location :
                                    if len(pred_location[voisin2]) != 0 :
                                        for i in location[voisin1] :
                                            if i in pred_location[voisin2] :
                                                #On peut dire que node a l'attribut i
                                                if not i in pred_location[node]:
                                                    pred_location[node].append(i)
                            elif voisin1 in pred_location :
                                if len(pred_location[voisin1]) != 0 :
                                    for i in pred_location[voisin1] :
                                        if voisin2 in location:
                                            if i in location[voisin2]:
                                                #On peut dire que node a l'attribut i
                                                if not i in pred_location[node]:
                                                    pred_location[node].append(i)
                                        elif voisin2 in pred_location :
                                            if len(pred_location[voisin2]) != 0:
                                                if i in pred_location[voisin2]:
                                                    #On peut dire que node a l'attribut i
                                                    if not i in pred_location[node]:
                                                        pred_location[node].append(i)
                            #College

                            if voisin1 in college :
                                if voisin2 in college:
                                    for i in college[voisin1] :
                                        if i in college[voisin2] :
                                            #On peut dire que node a l'attribut i
                                            if not i in pred_college[node]:
                                                pred_college[node].append(i)
                                elif voisin2 in pred_college :
                                    if len(pred_college[voisin2]) != 0 :
                                        for i in college[voisin1] :
                                            if i in pred_college[voisin2] :
                                                #On peut dire que node a l'attribut i
                                                if not i in pred_college[node]:
                                                    pred_college[node].append(i)
                            elif voisin1 in pred_college :
                                if len(pred_college[voisin1]) != 0 :
                                    for i in pred_college[voisin1] :
                                        if voisin2 in college:
                                            if i in college[voisin2]:
                                                #On peut dire que node a l'attribut i
                                                if not i in pred_college[node]:
                                                    pred_college[node].append(i)
                                        elif voisin2 in pred_college :
                                            if len(pred_college[voisin2]) != 0:
                                                if i in pred_college[voisin2]:
                                                    #On peut dire que node a l'attribut i
                                                    if not i in pred_college[node]:
                                                        pred_college[node].append(i)
                            #Employer
                            if voisin1 in employer :
                                if voisin2 in employer:
                                    for i in employer[voisin1] :
                                        if i in employer[voisin2] :
                                            #On peut dire que node a l'attribut i
                                            if not i in pred_employer[node]:
                                                pred_employer[node].append(i)
                                elif voisin2 in pred_employer :
                                    if len(pred_employer[voisin2]) != 0 :
                                        for i in employer[voisin1] :
                                            if i in pred_employer[voisin2] :
                                                #On peut dire que node a l'attribut i
                                                if not i in pred_employer[node]:
                                                    pred_employer[node].append(i)
                            elif voisin1 in pred_employer :
                                if len(pred_employer[voisin1]) != 0 :
                                    for i in pred_employer[voisin1] :
                                        if voisin2 in employer:
                                            if i in employer[voisin2]:
                                                #On peut dire que node a l'attribut i
                                                if not i in pred_employer[node]:
                                                    pred_employer[node].append(i)
                                        elif voisin2 in pred_employer :
                                            if len(pred_employer[voisin2]) != 0:
                                                if i in pred_employer[voisin2]:
                                                    #On peut dire que node a l'attribut i
                                                    if not i in pred_employer[node]:
                                                        pred_employer[node].append(i)
                        
                
                #Les lignes qui suivent inferent sur le principe suivant
                #Si un attribut se repete chez un grand nombre de voisin, il est très succeptible que nous l'ayons
                
                #Trouver une location a partir d'autres attributs deja predits
                for col in pred_college[node] :
                    for loc in all_locations :
                        if name_in_location(loc,col) :
                            #Si col est dans une certaine location (loc) alors on ajoute loc
                            pred_location[node].append(loc)
                for emp in pred_employer[node] :
                    for loc in all_locations :
                        if name_in_location(loc,emp) :
                            #Si emp est dans une certaine location (loc) alors on ajoute loc
                            pred_location[node].append(loc)
                #Trouver d'autres attributs a partir des locations
                for loc in pred_location[node] :
                    col_in_loc = attr_in_location(loc,"college")
                    for col in col_in_loc:  
                        for vois in G.neighbors(node):
                            if vois in college :
                                if col in college[vois] : #Si un voisin a cet attribut
                                    if not col in pred_college[node] : #Ajout dans la prediction
                                        pred_college[node].append(col)
                                elif vois in pred_college:
                                    if col in pred_college[vois] :
                                        if not col in pred_college[node] : #Ajout dans la prediction
                                            pred_college[node].append(col)
                    #La meme pour employer
                    emp_in_loc = attr_in_location(loc,"employer")
                    for emp in emp_in_loc:  
                        for vois in G.neighbors(node):
                            if vois in employer :
                                if emp in employer[vois] : #Si un voisin a cet attribut
                                    if not emp in pred_employer[node] : #Ajout dans la prediction
                                        pred_employer[node].append(emp)
                                elif vois in pred_employer:
                                    if emp in pred_employer[vois] :
                                        if not emp in pred_employer[node] : #Ajout dans la prediction
                                            pred_employer[node].append(emp)
                    
            
        '''

def naive_method(graph, empty, attr):

    predicted_values={}
    for n in empty:
        nbrs_attr_values=[] 
        for nbr in graph.neighbors(n):
            if nbr in attr:
                for val in attr[nbr]:
                    nbrs_attr_values.append(val)
        predicted_values[n]=[]
        if nbrs_attr_values: # non empty list
            # count the number of occurrence each value and returns a dict
            cpt=Counter(nbrs_attr_values)
            # take the most represented attribute value among neighbors
            a,nb_occurrence=max(cpt.items(), key=lambda t: t[1])
            predicted_values[n].append(a)
    return predicted_values

def evaluation_accuracy(groundtruth, pred):

    true_positive_prediction=0   
    for p_key, p_value in pred.items():
        if p_key in groundtruth:
            # if prediction is no attribute values, e.g. [] and so is the groundtruth
            # May happen
            if not p_value and not groundtruth[p_key]:
                true_positive_prediction+=1
            # counts the number of good prediction for node p_key
            # here len(p_value)=1 but we could have tried to predict more values
            true_positive_prediction += len([c for c in p_value if in_list(c,groundtruth[p_key])])      
        # no else, should not happen: train and test datasets are consistent
    return true_positive_prediction*100/sum(len(v) for v in pred.values())



for node in empty_nodes: 
                #Trouver une location a partir d'autres attributs deja predits
                if len(pred_location[node]) !=1 :  #S'il n'a encore aucune prediction  
                    for col in pred_college[node] :
                        for loc in all_locations :
                            if name_in_location(loc,col) :
                                #Si col est dans une certaine location (loc) alors on ajoute loc
                                pred_location[node].append(loc)
                    for emp in pred_employer[node] :
                        for loc in all_locations :
                            if name_in_location(loc,emp) :
                                #Si emp est dans une certaine location (loc) alors on ajoute loc
                                pred_location[node].append(loc)
                #Trouver d'autres attributs a partir des locations
                for loc in pred_location[node] :
                    if len(pred_college[node]) !=1 :
                        col_in_loc = attr_in_location(loc,"college")
                        for col in col_in_loc:  
                            for vois in G.neighbors(node):
                                if vois in college :
                                    if col in college[vois] : #Si un voisin a cet attribut
                                        if not col in pred_college[node] : #Ajout dans la prediction
                                            pred_college[node].append(col)
                                    elif vois in pred_college:
                                        if col in pred_college[vois] :
                                            if not col in pred_college[node] : #Ajout dans la prediction
                                                pred_college[node].append(col)
                    #La meme pour employer
                    if len(pred_employer[node]) !=1 :
                        emp_in_loc = attr_in_location(loc,"employer")
                        for emp in emp_in_loc:  
                            for vois in G.neighbors(node):
                                if vois in employer :
                                    if emp in employer[vois] : #Si un voisin a cet attribut
                                        if not emp in pred_employer[node] : #Ajout dans la prediction
                                            pred_employer[node].append(emp)
                                    elif vois in pred_employer:
                                        if emp in pred_employer[vois] :
                                            if not emp in pred_employer[node] : #Ajout dans la prediction
                                                pred_employer[node].append(emp)
                prob_required = 0
                #emp=>col
                if len(pred_college[node]) !=1 :
                    if len(pred_employer[node]) != 0:
                        best_col = all_colleges[0]
                        best_prob = corr_emp_col(pred_employer[node][0],best_col)
                        for emp in pred_employer[node] :
                            for col in all_colleges :
                                if best_prob < corr_emp_col(emp,col) :
                                    best_prob = corr_emp_col(emp,col)
                                    best_col = col
                        if not best_col in pred_college[node] and best_prob >= prob_required :
                            pred_college[node].append(best_col)

                #col=>emp
                if len(pred_employer[node]) !=1 :
                    if len(pred_college[node]) != 0:
                        best_emp = all_employers[0]
                        best_prob = corr_col_emp(pred_college[node][0],best_emp)
                        for col in pred_college[node] :
                            for emp in all_employers :
                                if best_prob < corr_col_emp(col,emp) :
                                    best_prob = corr_col_emp(col,emp)
                                    best_emp = emp
                        if not best_emp in pred_employer[node] and best_prob >= prob_required :
                            pred_employer[node].append(best_emp)
pred_college = naive_method(G,empty_nodes,college)
pred_employer = naive_method(G,empty_nodes,employer)
pred_location = naive_method(G,empty_nodes,location)          

print("Resultat : ")
groundtruth_employer={}
with open('mediumEmployer.pickle', 'rb') as handle:
    groundtruth_employer = pickle.load(handle)
result_e=evaluation_accuracy(groundtruth_employer,pred_employer)
groundtruth_college={}
with open('mediumCollege.pickle', 'rb') as handle:
    groundtruth_college = pickle.load(handle)
result_c=evaluation_accuracy(groundtruth_college,pred_college)
groundtruth_location={}
with open('mediumLocation.pickle', 'rb') as handle:
    groundtruth_location = pickle.load(handle)
result_l=evaluation_accuracy(groundtruth_location,pred_location)
print("College : ",result_c)
print("Employer : ",result_e)
print("Location : ",result_l)
#print(pred_college)

cpt = 0
for i in all_colleges :
    for loc in all_locations :
        if name_in_location(loc,i):
            cpt +=1
            break
print("Pourcentage : ",cpt)