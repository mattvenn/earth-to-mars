from PIL import Image
from random import randint
image_file = "fade.png"
img = Image.open(image_file)
img_width = img.size[0]
img_height = img.size[1]
print("opened %s [%d x %d]" % (image_file,img_width,img_height))

#function that returns the average value of a region of pixels
def avg_region(image,box):
    region = image.crop(box)
    colors = region.getcolors(region.size[0]*region.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present

reg_size = 5
data = []
for i in range(100):
    x = randint(reg_size, img_width - reg_size)
    y = randint(reg_size, img_height - reg_size)
    box = (x - reg_size, y - reg_size, x + reg_size, y + reg_size) 
    avg = avg_region(img, box)
    avg = [a / 255.0 for a in avg]

    d = { 'xy':  (x,y),
        'c': avg,
        }
    data.append(d)

import pickle
with open('data.pkl', 'w') as fh:
    pickle.dump(data, fh)
