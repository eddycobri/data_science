import community
import pickle
import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_gexf("mediumLinkedin.gexf")
college={}
location={}
employer={}
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
    for k,val in attribut.items():
        for i in val:
            if i in new_dict:
                diction[k]= new_dict[i]

    return diction

    

def find_best_attribut (attribut): # pour déterminer l'attribut le plus renseigné
    best_attribut=""
    cpt_bl=0
    cpt=0
    list_of_all_attribut=[]
    for k in attribut:
        val=attribut[k]
        for i in val:
            list_of_all_attribut.append(i)
            if attribut==location and i=='san francisco bay area':
                cpt+=1
        print(cpt)
        
    for l in list_of_all_attribut:
        cpt=0
        for i in list_of_all_attribut:
            if l == i:
                cpt+=1
        if cpt>=cpt_bl:
            cpt_bl=cpt
            best_attribut= l
        cpt=0
        
    return best_attribut,cpt_bl




best_location,n_location=find_best_attribut(location)
best_college,n_college=find_best_attribut(college)
best_employer,n_employer=find_best_attribut(employer)

print("la meilleure location est: "+str(best_location)+" il se repète %d  fois\n" % n_location)

print("le meilleur college est: "+str(best_college)+" il se repète %d  fois\n" % n_college)

print("le meilleur employer est: "+str(best_employer)+" il se repète %d  fois\n" % n_employer)



#je cherche now les plus centraux de chaque communauté: méthode 1

centrality_dict= nx.degree_centrality(G)

locat_part= attribut_partition(G, location)
partition = community.best_partition(G, locat_part, resolution=2., randomize=False)

value=[partition.get(node) for node in G.nodes()]
single_value=[]
centrality_value=0
maximum=0
for i in value:
    if i not in single_value:
        single_value.append(i)
for i in single_value:
    le_plus_centrique=''
    for k in partition:
        if partition[k]== i:
             if centrality_dict[k] > maximum:
                 maximum=centrality_dict[k]
                 le_plus_centrique=k
    maximum=0
    centrality_value=0
    print(" la communauté %d \n" %i)
    print("le_plus_centrique pour est :  %s \n" %le_plus_centrique)
#####""  



#je cherche now les plus centraux de chaque communauté: méthode 2

method2_centrality= nx.betweenness_centrality(G)

single_value=[]
list_centriqu=[]
centrality_value=0
maximum=0
for i in value:
    if i not in single_value:
        single_value.append(i)
for i in single_value:
    le_plus_centrique=''
    for k in partition:
        if partition[k]== i:
             if method2_centrality[k] > maximum:
                 maximum=method2_centrality[k]
                 le_plus_centrique=k
    list_centriqu.append(le_plus_centrique)

    maximum=0
    centrality_value=0
    print(" la communauté %d \n" %i)
    print("le_plus_centrique m pour est :  %s \n" %le_plus_centrique)

print(list_centriqu)
location={}
with open('mediumLocation.pickle', 'rb') as handle:
    location = pickle.load(handle)

for i in list_centriqu:
    print(location[i])
#####""  




#dessin
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

