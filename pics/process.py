from PIL import Image, ImageStat

def process(file_name):
    im = Image.open(file_name).convert('L')
    stat = ImageStat.Stat(im)
    return stat.rms[0]

for filename in ['black','grey','white']:
    print(filename, process(filename + ".jpg"))
