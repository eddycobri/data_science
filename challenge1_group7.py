# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
import pickle

# I am U19886 and I want to work at Google.
ME = 'U19886'

#We load the graph
G = nx.read_gexf("mediumLinkedin.gexf")

# load the profiles. 3 files for each type of attribute
# Some nodes in G have no attributes, or just location, or all of same
# Some nodes may have 2 or more colleges or employers, so we
# use dictionaries to store the attributes
college={}
location={}
employer={}
# The dictionaries are loaded as dictionaries from the disk (see pickle in Python doc)
with open('mediumCollege.pickle', 'rb') as handle:
    college = pickle.load(handle)
with open('mediumLocation.pickle', 'rb') as handle:
    location = pickle.load(handle)
with open('mediumEmployer.pickle', 'rb') as handle:
    employer = pickle.load(handle)

# Let's find all the node having Google as employer
google_guys = []
for k,v in employer.items():
    if (v[len(v)-1] == "Google") or (v[len(v)-1] == "google") : #If the last employer (The current actually) is "Google"
        google_guys.append(k)
        #print(k," est à Google!")
#Granettover says that the employer has more trust in people who spend the longest time in his company
#So let's get the list of Google employees who have always worked at Google
#ie. those who only get "Google" in their employers list
google_or_nothing_guys = []
for u in google_guys :
    if len(employer[str(u)])==1 : #If the google guys have only one item in their employers list
        google_or_nothing_guys.append(u)
#print("Google or nothing : ")
#print(google_or_nothing_guys)
'''
print("Moi")
print(location['U19886'])
print(college['U19886'])
print(location['U19886'])
for i in google_or_nothing_guys :
    print("#######################################################")
    print(i)
    print(location[str(u)])
    print(college[str(u)])
    print("#######################################################")'''

#Let's find all the guy from de same college than the Google guys
#Actually, the college seems (It's just our deduction) to be an important criterea to work at Google
#Because all the guys working there (and being 'loyal' to the company) are from the same college
#print("############################### COLLEGE GOOGLELIQUE#################################")
#print(college)
'''
for i in google_or_nothing_guys:
    
    try :
        print(str(i))
        print(college[str(i)])
    except Exception:
        print(str(i)+" n'a pas ecole")
    try :
        print(location[str(i)])
    except Exception :
        print(str(i)+" n'a pas location")
    
    try :
        print(str(i))
        print(college[str(i)])
        print(location[str(i)])

    except Exception:
        continue

    print("..........")
    
'''

######################################## Method One ###########################################
G_cpy = G.copy()
shortest_paths_to_google = []
for guy in google_guys :
    #We are going to remove all the nodes from the graph excepted the current "guy"
    for guy_to_remove in google_guys :
        if not (guy_to_remove == guy) :
            try :
                G_cpy.remove_node(str(guy_to_remove))
            except nx.NetworkXError :
                continue
    #From here I've  a graph (G_cpy) with one and only node from Google (guy)
    #I'm going to search for the shortest path from him (guy) to me ('U19886')
    try :
        shortest_paths_to_google.append(nx.dijkstra_path(G_cpy,ME,str(guy)))
    except nx.NetworkXNoPath : #If there is not any path between me and current guy
        continue
    G_cpy = G.copy() #We reload the initial graph for the next google guy
#print("Tous les plus courts chemins menant a un employe de Google")
#print(shortest_paths_to_google)
############### Displaying shortest paths###############
'''
i = 1
for path in shortest_paths_to_google :
    print("Chemin "+str(i)+"  ("+str(len(path))+"):")
    print(path)
    for d in path:
        try:
            print(college[str(d)])
        except Exception:
            continue
        
    i = i + 1
'''
'''
print(employer)
print(college)
print(location)
'''
############################## Methode Two ###########################

def college_in_common(guy):

    tab = []
    for k,v in college.items():
        try :
            if k == guy :
                continue
            else :
                for i in college[str(guy)] :
                    for j in v:
                        if i==j :
                            tab.append(k)
        except Exception :
            continue
    return tab

def location_in_common(guy):
    
    tab = []
    for k,v in location.items():
        try :
            if k == guy :
                continue
            else :
                for i in location[str(guy)] :
                    for j in v:
                        if i==j :
                            tab.append(k)
        except Exception :
            continue
    return tab
def employer_in_common(guy):
    
    tab = []
    for k,v in employer.items():
        try :
            if k == guy :
                continue
            else :
                for i in employer[str(guy)] :
                    for j in v:
                        if i==j :
                            tab.append(k)
        except Exception :
            continue
    return tab
    
''' #NEVER EVER RUN THIS CODE: ALMOST INFITE COMPUTATION TIME
for i in google_guys :
    for path in nx.all_simple_paths(G,ME,i) :
        print(path)'''

def h_pertinence(source,target): #Function that will be pass as heuristic parameter in a*
    point = 0 
    if source in employer_in_common(target):
        point=+3
    if source in location_in_common(target):
        point=+2
    if source in college_in_common(target):
        point=+4
    if point == 0 : #If the 2 nodes don't have anything in common we look at the neighbors of the tagert
        for nbr in G.neighbors(target):
            if target in employer_in_common(nbr):
                point=+2
            if target in location_in_common(nbr):
                point=+1
            if target in college_in_common(nbr):
                point=+3
            if not (point == 0) :
                break
    
    cost = 9-point    #The most of point we have the less we cost and the min of cost is 0
    return cost

 #Let's fing all the path from ME to all google_or_nothing_guys
G_cpy = G.copy()
shortest_star_paths_to_google = []
for guy in google_or_nothing_guys :
    #We are going to remove all the nodes from the graph excepted the current "guy"
    for guy_to_remove in google_or_nothing_guys :
        if not (guy_to_remove == guy) :
            try :
                G_cpy.remove_node(str(guy_to_remove))
            except nx.NetworkXError :
                continue
    #From here I've  a graph (G_cpy) with one and only node from Google (guy)
    #I'm going to search for the shortest path from him (guy) to me ('U19886')
    try :
        shortest_star_paths_to_google.append(nx.astar_path(G_cpy,ME,str(guy),heuristic=h_pertinence))
    except nx.NetworkXNoPath : #If there is not any path between me and current guy
        continue
    G_cpy = G.copy() #We reload the initial graph for the next google guy

#We just have to find the shortest path among all of those retrieved by A*
best_path = shortest_star_paths_to_google[0]

for path in shortest_star_paths_to_google:
    if len(path)<len(best_path):
        best_path = path
print("''''''''''''''''''''''''''''' LE MEILLEUR CHEMIN POUR AVOIR DU TRAVAIL A GOOGLE ''''''''''''''''''''''''''''''")
print([d for d in best_path],sep='==>')
print("Google guys : ")
print([d for d in google_or_nothing_guys])