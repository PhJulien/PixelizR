#!/usr/bin/python


#### Importing libraries and stuff
from PIL import Image, ImageEnhance
import random, sys
from optparse import OptionParser



#### Parsing arguments
usage = "usage: %prog -i InputFile -o OutputFile [-p 2]"
parser = OptionParser(usage=usage)

parser.add_option("-i", "--image", dest="ImageFile",
                  help="Input image to be treated", metavar="InputImage")
parser.add_option("-o", "--outfile", dest="OutFile",
                  help="Output image to be created", metavar="OutputImage")
parser.add_option("-p", "--percentage", dest="Perc", default=2, type="float",
                  help="Size of each 'pixel' in percentage of width (or height)", metavar="Perc")                  
                  
(options, args) = parser.parse_args()

## To do: check if percentage is integer
if not options.ImageFile or not options.OutFile:
    parser.error("Error. Please check all arguments are provided")
    exit()

#### Opening file

im = Image.open(options.ImageFile)


imDest2 = Image.new("RGB", im.size) #can add "white as 3rd argument to define background color"

# print "Perc=" + str((options.Perc/100)) + " - x step=" + str(im.size[0]  * (options.Perc/100)) + " - ystep=" + str(im.size[1]  * (options.Perc/100))

x_corners = range(0, im.size[0] + 1, int(im.size[0]  * (options.Perc/100))) # Might want to set this number as a parameter
y_corners = range(0, im.size[1] + 1, int(im.size[1]  * (options.Perc/100))) # Might want to set this number as a parameter
for i in range(0,len(x_corners)-1):
    for j in range(0,len(y_corners)-1): 
        thisBox = (
            x_corners[i], 
            y_corners[j], 
            x_corners[i+1], 
            y_corners[j+1]
            )
            
        region = im.crop(thisBox)
        width, height = region.size
        pixels = region.load()
        data = []
            
        for x in range(width):
            for y in range(height):
                cpixel = pixels[x, y]
                data.append(cpixel)
                
        r = 0
        g = 0
        b = 0
        counter = 0
        for x in range(len(data)):
        # if data[x][3] > 200: # Activate this if PNG
            r+=data[x][0]
            g+=data[x][1]
            b+=data[x][2]
            counter+=1;      
                         
        rAvg = r/counter
        gAvg = g/counter
        bAvg = b/counter
            
        newPixel = Image.new("RGB", region.size, (rAvg, gAvg, bAvg))
        imDest2.paste(newPixel, thisBox)


imDest2.save(options.OutFile)

