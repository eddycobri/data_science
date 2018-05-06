import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import numpy as np
import pickle
from collections import Counter
from networkx.algorithms import community as com
import community
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import challenge2_skeleton

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
def compare_string(string_one,string_two):
    no_relevent_words = ["at","of","in","for","and","area","city","town"]
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

#################################################
######       DATA PREPARATION             #######
#################################################


#List of colleges
all_colleges = []
for k,v in college.items() :
    for i in v :
        if not (i in all_colleges) :
            all_colleges.append(i)
'''
print("########################### ALL COLLEGES IN THE WORLD ###########################")
cpte = 0
for i in all_colleges :
    cpte +=1
    print(cpte," => ",i)
    if name_in_location("illinois",i):
        print("Dans illinois!")
    
'''
print(location)
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
    #print(cpte," => ",i)

#List of Emloyer
all_employers = []
for k,v in employer.items() :
    for i in v :
        if not (i in all_employers) :
            all_employers.append(i)
'''
print("########################### ALL EMPLOYER IN THE WORLD ###########################")
cpte = 0
for i in all_employers :
    cpte +=1
    print(cpte," => ",i)



This function compare two long strings decomposing them into 'pertinent' words


'''


#Method 1
#Use homophily
list_3_clique = com.k_clique_communities(G,3)
print(list(list_3_clique))

def homophily_based_method(dic_attribute):
    for node in G.nodes():
        for voisin in G.neighbors(node) :
            print("something")

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
print("Partly profiled : ",find_partly_profile(G))

print("######## Tous les gars avec les profiles complets #########")
eux_tous = find_complete_profile(G)
#print(eux_tous)
print("Ils sont ", len(eux_tous))
print("Soit : ",(len(eux_tous)/811)*100)
print("######## Tous les gars avec les profiles partiellement remplis #########")
truc = find_partly_profile(G)
print("Les autres qui ont un peu mais pas tout XD sont : ",(len(truc)/811)*100)


         

#Tableau NodeXLocation
#Let's get all value for a given attribute

def get_all_values(attribute):
    all_attributes = []
    
    for values in attribute.values():
        for val in values:
            already_in = False
            for i in all_attributes:
                if compare_string(val,i) : #If val is already in all_attributes
                    already_in = True
                    break
            if already_in :
                break
            else :
                all_attributes.append(val)
    return all_attributes



###################### Method One ##################

#Creation of the Matrix
#Location
def create_matrix(attribute):
    guys = {}
    all_attributes = get_all_values(attribute)
    for node in G.nodes():
        tmp_list = []
        for attr in all_attributes :
            if not (node in attribute) :
                tmp_list.append([attr,0])
        if not (len(tmp_list) == 0) :
            guys[node] = tmp_list
    return guys
def set_matrix_value(matrix,attribute,node,value):
    if attribute in all_colleges :
        #We must consider the college matrix
        for guy in matrix:
            if guy == node : #If we reach the guy we want in the matrix
                for col in matrix[guy]:
                    if col[0] == attribute : #If we reach the right attribute corresponding to the guy
                        col[1] = value #We update the value
                        return True
    elif attribute in all_employers :
        #We must consider the employer matrix
        for guy in matrix:
            if guy == node : #If we reach the guy we want in the matrix
                for emp in matrix[guy]:
                    if emp[0] == attribute : #If we reach the right attribute corresponding to the guy
                        emp[1] = value #We update the value
                        return True
    elif attribute in all_locations :
        #We must consider the location matrix
        for guy in matrix:
            if guy == node : #If we reach the guy we want in the matrix
                for loc in matrix[guy]:
                    if loc[0] == attribute : #If we reach the right attribute corresponding to the guy
                        loc[1] = value #We update the value
                        return True

def get_matrix_value(matrix,attribute,node):
    if attribute in all_colleges :
        #We must consider the college matrix
        for guy in matrix:
            if guy == node : #If we reach the guy we want in the matrix
                for col in matrix[guy]:
                    if col[0] == attribute : #If we reach the right attribute corresponding to the guy
                        return col[1]
    elif attribute in all_employers :
        #We must consider the employer matrix
        for guy in matrix:
            if guy == node : #If we reach the guy we want in the matrix
                for emp in matrix[guy]:
                    if emp[0] == attribute : #If we reach the right attribute corresponding to the guy
                        return emp[1]
    elif attribute in all_locations :
        #We must consider the location matrix
        for guy in matrix:
            if guy == node : #If we reach the guy we want in the matrix
                for loc in matrix[guy]:
                    if loc[0] == attribute : #If we reach the right attribute corresponding to the guy
                        return loc[1]


'''
M_loc = create_matrix(location)
for i,j in M_loc.items() :
    print(i," => ",j)'''
'''
TODO
- Modify function name_in_location() regarding the fact that a location has the following structure :
    district town state country
def inference_method_one():
    #Le truc qui va noter les trucs

'''

#Relation between location=>employer=>college=>employer
#1
'''

This function take as parameter an attribute (actually a dictionary) either 'college' or 'employer'
If a location is contained in an attribute name then we add the attriute in the field of the
dictionary (which will be returned) having as key the location
'''

def in_location(attribute):
    list_to_return = {}
    all_location = get_all_values(location)
    for loc in all_location : #Pour chaque valeur de location
        attribute_in_loc = []
        for v in attribute.values() : #On cherche tous les attributs qui contiennent dans leur denomination, une localisation
            for val in v : #Pour chaque valeur de l'attribut 'employer' ou 'college'
                if name_in_location(loc,val) :
                    attribute_in_loc.append(val)
        list_to_return[loc] = attribute_in_loc 
    return list_to_return


print("------------------------  Rélation location−employer --------------------")
#print(in_location(employer))
print("------------------------  Rélation location−college --------------------")
#print(in_location(college))

####### Test hypotheses 
'''
    The following code snippet test how many nodes among the "completely profiled" don't respect the
    following assesment :
    Two conected guys share at least one attribute or one friend

non_respect_counter = 0
for node in G.nodes():
    if node in eux_tous :
        for nb in nodes.neighbors()
'''

def completely_profiled(g,attribute):
    '''
    This function take as parameter a graph and and an attribute (dict) and return True if all 
    the nodes of the graph have at least one value of the given attribute
    '''
    for node in g.nodes():
        if not node in attribute :
            #If current guy is not in the dict that is if he doesn't have that attribute ...
            return False
            #Because everybody must at least one attribute
        else :
            if len(attribute[node]) == 0 :
                return False #If there's not value yet in the list
    return True

g_cpy = G.copy() #Copy of the graph

def infer_location():
    global location
    global college
    global employer
    global g_cpy
    for node in g_cpy.nodes():
        
        if (not node in location) and (node in college or node in employer):
            
            if node in college :
                #college[node].reverse()
                for col in college[node] :
                    for loc in all_locations:
                        if name_in_location(loc,col) : #Le mec il habite dans cette location
                            location[node] = [loc] #On lui donne la valeur de la location
                            break
                    if node in location : #Si on lui a donné la valeur
                        break
                #college[node].reverse()
            else :
                #employer[node].reverse()
                for emp in employer[node] :
                    for loc in all_locations:
                        if name_in_location(loc,emp) : #Le mec il habite dans cette location
                            location[node] = [loc] #On lui donne la valeur de la location
                            break
                    if node in location : #Si on lui a donné la valeur
                        break
                #employer[node].reverse()
print(len([guy for guy in location]))
infer_location()

print("Apres infer")
print(len([guy for guy in location]))
location_matrix = create_matrix(location)
employer_matrix = create_matrix(employer)
college_matrix = create_matrix(college)
set_matrix_value(location_matrix,"norfolk virginia area",'U22820',36)
#print(location_matrix)
#print(get_matrix_value(location_matrix,"norfolk virginia area",'U22820'))

sortie = False
required_note = 2
while not sortie :
    for loc in all_locations:
        for node in g_cpy.nodes():
            if node in location_matrix.keys() and not node in location:
                nb_voisins_att = 0
                nb_voisins = 0
                for voisin in g_cpy.neighbors(node):
                    if voisin in location :
                        nb_voisins_att +=1
                    nb_voisins +=1
                note = (nb_voisins_att/nb_voisins)*10
                set_matrix_value(location_matrix,loc,node,note)
    for col in all_colleges:
        for node in g_cpy.nodes():
            if node in college_matrix.keys() and not node in college:
                nb_voisins_att = 0
                nb_voisins = 0
                for voisin in g_cpy.neighbors(node):
                    if voisin in college :
                        nb_voisins_att +=1
                    nb_voisins +=1
                note = (nb_voisins_att/nb_voisins)*10
                set_matrix_value(college_matrix,col,node,note)
                
    for emp in all_employers:
        for node in g_cpy.nodes():
            if node in employer_matrix.keys() and not node in employer:
                nb_voisins_att = 0
                nb_voisins = 0
                for voisin in g_cpy.neighbors(node):
                    if voisin in employer :
                        nb_voisins_att +=1
                    nb_voisins +=1
                note = (nb_voisins_att/nb_voisins)*10
                set_matrix_value(employer_matrix,emp,node,note)
    #Check all the matrix and add all the attribute having at least 5 as note to the node corresponding
    '''
    to_remove_from_matrix = []
    for k,v in location_matrix.items():
        for j in range(0,len(v)):
            if v[j][1] >= required_note :
                if k in location :
                    location[k].append(v[j][0])
                else :
                    location[k] = []
                    location[k].append(v[j][0])
                #Remove the element from the matrix
                #location_matrix[k].remove(v[0])
                to_remove_from_matrix.append([k,v[j][0]])
    for i in to_remove_from_matrix :
        location_matrix[i[0]].remove(i[1])
        if len(location_matrix[i[0]]) == 0 :
            #Virer node de la matrice
            del location_matrix[i[0]]

    #to_remove_from_matrix = []
    for k,v in college_matrix.items():
        for j in range(0,len(v)):
            if v[j][1] >= required_note :
                if k in college :
                    college[k].append(v[j][0])
                else :
                    college[k] = []
                    college[k].append(v[j][0])
                #Remove the element from the matrix
                #location_matrix[k].remove(v[0])
                to_remove_from_matrix.append([k,v[j][0]])
    for i in to_remove_from_matrix :
        college_matrix[i[0]].remove(i[1])
        if len(college_matrix[i[0]]) == 0 :
            #Virer node de la matrice
            del college_matrix[i[0]]
    
    #to_remove_from_matrix = []
    for k,v in employer_matrix.items():
        for j in range(0,len(v)):
            if v[j][1] >= required_note :
                if k in employer :
                    employer[k].append(v[j][0])
                else :
                    employer[k] = []
                    employer[k].append(v[j][0])
                #Remove the element from the matrix
                #location_matrix[k].remove(v[0])
                to_remove_from_matrix.append([k,v[j][0]])
    for i in to_remove_from_matrix :
        employer_matrix[i[0]].remove(i[1])
        if len(employer_matrix[i[0]]) == 0 :
            #Virer node de la matrice
            del employer_matrix[i[0]]'''

    sortie = completely_profiled(g_cpy,employer) and completely_profiled(g_cpy,college) and completely_profiled(g_cpy,location)
    print("Boucle!")
print("FINI!")
# --------------------- Baseline method -------------------------------------#
# Try a naive method to predict attribute
# This will be a baseline method for you, i.e. you will compare your performance
# with this method
# Let's try with the attribute 'employer'
groundtruth_employer={}
with open('mediumEmployer.pickle', 'rb') as handle:
    groundtruth_employer = pickle.load(handle)
result_e=challenge2_skeleton.evaluation_accuracy(groundtruth_employer,employer)
groundtruth_college={}
with open('mediumCollege.pickle', 'rb') as handle:
    groundtruth_college = pickle.load(handle)
result_c=challenge2_skeleton.evaluation_accuracy(groundtruth_college,college)
groundtruth_location={}
with open('mediumLocation.pickle', 'rb') as handle:
    groundtruth_location = pickle.load(handle)
result_l=challenge2_skeleton.evaluation_accuracy(groundtruth_location,location)

print("-------------------------- RESULTAT ---------------")
print("Employer : ",result_e)
print("College : ",result_c)
print("Location : ",result_l)