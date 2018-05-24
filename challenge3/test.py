from PIL import Image
import numpy as np

input_filename = "population-density-map.bmp"

the_map = Image.open(input_filename)

matrix = np.array(the_map)

width = the_map.size[0]
heigth = the_map.size[1]
"""
def get_point(coor_x,coor_y):
    global width
    global heigth

    for x in range(width):
        for y in range(heigth):
            if x == coor_x and y == coor_y :
                return 
"""



def get_color(x,y):

    global width
    global heigth

    global the_map
    
    global matrix

    for i_x in range(width):
        for i_y in range(heigth):
            if x == i_x and y == i_y :
                return matrix[x,y]


def get_point(color):
    
    global width
    global heigth

    global the_map
    
    global matrix

    for i_x in range(width):
        for i_y in range(heigth):
            if np.array_equal(matrix[i_y,i_x],np.array(color)) :
                return (i_x,i_y)


#print(get_point([0,255,0])) #Coordonnées du point vert (4426, 2108)
#print(get_point([255,0,0])) #Coordonnées du point rouge (669, 1306)