# -*- coding: utf-8 -*-
import networkx as nx
import numpy as np
import pickle

# I am U19886 and I want to work at Google.


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
print("############################### COLLEGE GOOGLELIQUE#################################")
#print(college)
'''
for k,v in college.items():
    try :
        if "tongji university" in v:
            print(k)
            print(v)
            print("_____________________________________________")
    except Exception:
        continue'''

print("..........................")
for i in google_guys:
    try :
        print(str(i))
        print(college[str(i)])
    except Exception:
        print(str(i)+" n'a pas ecole")
    try :
        print(location[str(i)])
    except Exception :
        print(str(i)+" n'a pas location")
    print("..........")

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
        shortest_paths_to_google.append(nx.dijkstra_path(G_cpy,'U19886',str(guy)))
    except nx.NetworkXNoPath : #If there is not any path between me and current guy
        continue
    G_cpy = G.copy() #We reload the initial graph for the next google guy
print("Tous les plus courts chemins menant a un employe de Google")
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