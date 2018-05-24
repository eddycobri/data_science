from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


input_filename="/home/rudy/Desktop/population-density-map.bmp"

the_map = Image.open(input_filename)


matrix = np.array(the_map)
the_map_gray=the_map.convert('L')
the_map_gray.save('themapgray.bmp')
gray_matrix=np.array(the_map_gray)
print(matrix)
print(gray_matrix[0][4])



"""
def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

img = mpimg.imread('image.png')     
gray = rgb2gray(img)    
plt.imshow(gray, cmap = plt.get_cmap('gray'))
plt.show()
"""