from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.graph import route_through_array
import networkx as nx

input_filename="C:/population-density-map.bmp"

the_map = Image.open(input_filename)
width=the_map.size[0]
heigth=the_map.size[1]
matrix = np.array(the_map)
the_map_gray=the_map.convert('L')
the_map_gray.save('themapgray.bmp')
gray_matrix=np.array(the_map_gray)
#print(matrix)
#print(gray_matrix)

brest=[2108,4426]  #coor de brest 
rize=[1306,669]          # coor de rize


#the_map_gray.show()
colors = the_map_gray.getcolors(width*heigth)
print('Nb of different colors: %d' % len(colors))


#la fo²nction si_dessous permet de reduire une matrice...

def matrix_transformer (the_matrix, n):
    new_matrix=[]
    (x,y)=np.shape(the_matrix)
    z,t=0,0
    while z<x:
        ligne=[]
        while t<y:
            #print(the_matrix[z:z+n,t:t+n])
            moy=np.mean(the_matrix[z:z+n,t:t+n])
            #print("la moyenne est :"+str(moy)+" pour "+ str(t)+"\n")
            ligne.append(moy)
            t+=n
        new_matrix.append(np.array(ligne))
        #print("000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000  ")
        z+=n
    return np.array(new_matrix)            
    

def my_graph(matrice):
    """
    matrice - matrix array : gray matrix of the image
    Output : This function returns a graph (grid 2D with tuple (line, column) as nodes) with the time to parse 2 neighbour nodes as weight 

    """
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


# from gray colors to density
density = gray_matrix/255.0
print(density)
#reduced_density=matrix_transformer(density, 10)
#print(reduced_density)
a=np.size(density)
print(a)
b=np.shape(density)
print(b)

"""
#the shortest path used by the zombie for Rize to brest is the path consisted of city with higher density , so
the_path=route_through_array(density, rize, brest)
print(the_path)
pixelArray = the_map.load() # pixel array
print("00000000000000000000")
print(the_path[0])
plt.imshow(density)
plt.plot(4426,2108,'g*')
plt.plot(669,1306,'g*')
for i in the_path[0]:
    plt.plot(i[1],i[0],'r*')
	#pixelArray[i[1],i[0]] = (254, 107, 0, 100) # change pixel color
#the_map.show()
plt.axis('off')
plt.show() 
"""
"""
for i,j in th
plt.imshow(density)
plt.plot(4426,2108,'r*')
plt.plot(669,1306,'r*')
plt.axis('off')
plt.show() #show the map with Brest and Turkey
""" 

"""
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

img = mpimg.imread('image.png')     
gray = rgb2gray(img)    
plt.imshow(gray, cmap = plt.get_cmap('gray'))
plt.show()
"""


