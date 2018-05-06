import community
import pickle
import networkx as nx
import matplotlib.pyplot as plt
#from openpyxl import Workbook


#better with karate_graph() as defined in networkx example.
#erdos renyi don't have true community structure
#G = nx.erdos_renyi_graph(30, 0.05)
G = nx.read_gexf("mediumLinkedin.gexf")
#first compute the best partition
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



def attribut_partition (graph, attribut):
    new_dict={}
    diction=attribut
    list_of_all_attribut=[]
    for k,val in attribut.items():
        for i in val:
            if not i in list_of_all_attribut:
                list_of_all_attribut.append(i)
    match=0  #just pour faire le remplissage

    for  i in list_of_all_attribut:
        new_dict[i] = match
        match+=1
    #print(new_dict)
    for k,val in attribut.items():
        for i in val:
            if i in new_dict:
                diction[k]= new_dict[i]

    return diction


       
    












"""calcule de la centralité:"""
centrality_dict= nx.degree_centrality(G)

locat_part= attribut_partition(G, location)

partition = community.best_partition(G, locat_part)
value=[partition.get(node) for node in G.nodes()]

print(value)
print("\n\n")

#print(locat_part)
#print(centrality_dict)

#print(partition)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


nx.draw_networkx_edges(G,pos, alpha=0.5)
plt.show()

