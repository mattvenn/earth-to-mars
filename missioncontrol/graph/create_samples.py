from PIL import Image
from config_real import SAMPLE_TYPES
from config_real import MAX_X as maxx
from config_real import MAX_Y as maxy


#function that returns the average value of a region of pixels
def avg_region(image,box):
    region = image.crop(box)
    colors = region.getcolors(region.size[0]*region.size[1])
    max_occurence, most_present = 0, 0
    for c in colors:
        if c[0] > max_occurence:
            (max_occurence, most_present) = c
    return most_present

for sample_type in SAMPLE_TYPES.keys():
    SAMPLE_TYPES[sample_type]['img'] = Image.open(sample_type + ".png")
    print("%s" % (sample_type))

print SAMPLE_TYPES
exit()

reg_size = 5
samples = [[x for x in range(maxx)] for y in range(maxy)]

# prepare dataset
with open("rfid.txt") as fh:
    rfids = fh.readlines()
rfids = [rfid.strip() for rfid in rfids]

for x in range(0,maxx):
    for y in range(0,maxy):
        index = y + x * maxy
        samples[y][x] = { 'rfid' : rfids[index] }
        for sample_type in SAMPLE_TYPES.keys():

            xpix = SAMPLE_TYPES[sample_type]['img'].size[0] / maxx * x
            ypix = SAMPLE_TYPES[sample_type]['img'].size[1] / maxy * y
            box = (xpix - reg_size, ypix - reg_size, xpix + reg_size, ypix + reg_size) 
            avg = avg_region(SAMPLE_TYPES[sample_type]['img'], box)
            samples[y][x][sample_type] = avg[0] / 255.0 * SAMPLE_TYPES[sample_type]['max']
    
        print(samples[y][x])

# reformat for robots
robot_hash = {}
for x in range(0,maxx):
    for y in range(0,maxy):
        sample_data = samples[y][x]
        sample_data['x'] = x
        sample_data['y'] = y
        rfid = sample_data['rfid']

        del(sample_data['rfid'])

        robot_hash[rfid] = sample_data
        
#print robot_hash

import json
with open('sample_data.json', 'w') as fh:
    json.dump(robot_hash, fh, indent=0)
