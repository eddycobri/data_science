from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skimage.graph import route_through_array

input_filename="/home/rudy/Desktop/population-density-map.bmp"

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


the_map_gray.show()
colors = the_map_gray.getcolors(width*heigth)
print('Nb of different colors: %d' % len(colors))



# from gray colors to density
density = gray_matrix/255.0

#the shortest path used by the zombie for Rize to brest is the path consisted of city with higher density , so
the_path=route_through_array(density, rize, brest)

pixelArray = the_map.load() # pixel array
for i in the_path[0]:
	pixelArray[i[1],i[0]] = (255,0,0,255) # change pixel color
the_map.show()



print(density)
"""
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

