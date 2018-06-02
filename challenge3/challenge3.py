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
brest=[2108,4426]  #coor de brest 
rize=[1306,669]          # coor de rize

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

