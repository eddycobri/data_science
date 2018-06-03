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
