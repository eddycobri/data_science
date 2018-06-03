from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.graph import route_through_array
import networkx as nx

input_filename="population-density-map.bmp"

the_map = Image.open(input_filename)
width=the_map.size[0]
heigth=the_map.size[1]
matrix = np.array(the_map)
the_map_gray=the_map.convert('L')
the_map_gray.save('themapgray.bmp')
gray_matrix=np.array(the_map_gray)
rize=[2108,4426]  #coor de brest 
brest=[1306,669]          # coor de rize

max_gray_level = np.amax(gray_matrix)
density_matrix = gray_matrix / 255.0
shortest_path = route_through_array(density_matrix,rize,brest)
colors = the_map_gray.getcolors(width*heigth)


#the shortest path used by the zombie for Rize to brest is the path consisted of city with higher density , so
the_path=route_through_array(1./density_matrix, rize, brest) #we use the inverse for take the pixel with higher density

pixelArray = the_map.load() # pixel array
plt.imshow(density_matrix)
for i in the_path[0]:   
    plt.plot(i[1],i[0],'w*')
plt.axis('off')
plt.show() 

def find_time(path,density): #this function permit to determine the duration of the travel of zombies
    the_duration=0
    null_density=0
    for area in path[0]: #go through the path
        pxl_density=density[area[0],area[1]] # take the density of the pixel
        if (pxl_density==0):
            print(area)

        speed=(23/24)*pxl_density+ (1/24) # caculate the speed of the zombie in this area
        the_duration+=1/speed # compute the duration
    print("null density = : "+str(null_density))
    days=the_duration//24
    hour=the_duration%24
    hours=hour%60
    months=days//30
    days=days%30
    
    return (months,days,hours)


info_duration=find_time(the_path,density_matrix)
print(info_duration)

def matrix_transformer (the_matrix, n):# this function permit to reduce a matrix for manipulating easily
    new_matrix=[]
    (x,y)=np.shape(the_matrix)
    z,t=0,0
    while z<x:
        ligne=[]
        while t<y:
            moy=np.mean(the_matrix[z:z+n,t:t+n]) # we taque the mean of a bloc of mthe matrix and 
            ligne.append(moy)#atribute it at a new value
            t+=n
        new_matrix.append(np.array(ligne))
        z+=n
    return np.array(new_matrix)    

 ################### Méthode 2 with graph..................   

def my_graph(matrice):
    
    G = nx.grid_2d_graph(0,0) #new graph
    densitym = matrice/255.0 #density matrix
    heigth = matrice.shape[0] #heigth and width of the matrix
    width = matrice.shape[1]   
    for i in range (heigth): 
        for j in range (width):
            
            G.add_node((i,j)) #we add the nodes (i,j) with i the line and j the column
            print((i,j))
    for node in list(G.nodes):
        i = node[0]
        j = node[1]
        ends = [[i+1,j],[i,j+1],[i-1,j],[i,j-1]] #neighbours of node (i,j)
        for end in ends:
            if (end[0]>=0 and end[0]<heigth) and (end[1]>=0 and end[1]<width):
                speed=(1+23*(densitym[end[0], end[1]]))/24   #la vitesse des zombie
                G.add_edge((i,j),(end[0],end[1]),weight = 1/float(speed)) #we add the edge between (i,j) and each neighbour with the time as weight
    nx.draw(G)
    plt.show()
    return G



graph=my_graph(gray_matrix)
the_path2= nx.dijkstra_path(graph,str(2108,4426),str(1306,669))
print(the_path2)
info_duration2=find_time(the_path2,density_matrix)


