#!/usr/bin/python

from PIL import Image, ImageEnhance
import random, math, sys

outdir="/Users/pjulien/Code/Pan/Out/"

imageFile = "/Users/pjulien/Code/Pan/Original/S.jpg"
im = Image.open(imageFile)

ext = ".jpg"
sigma_brightness = 0.25
sigma_contrast = 0.3
sigma_pixels = 20
sigma_pixels2 = 8
rotate = True

######
######
###### Functions
######


def crop_and_paste(imOri, imDest, box, brightness, contrast):
    #print str(brightness)
    
    box = list(box)
    for i in range(0, len(box)):
        if (box[i] < 0):
            box[i] = 0
            
    surface = abs(box[2] + box[0]) * abs(box[3] + box[1])
    if surface:
        print "Box: " + str(box) + " - Surface: " + str(surface)
        print "Width: " + str(abs(box[2] + box[0])) + " - Height: " + str(abs(box[3] + box[1]))
        region = im.crop(box)
        
        
        # Changing brightness
        bright = ImageEnhance.Brightness(region)
        region = bright.enhance(brightness)
        
        # Changing contrast
        contr = ImageEnhance.Contrast(region)
        region = contr.enhance(contrast)
    
        # Pasting region to destination image
        imDest.paste(region, box)
        return(imDest)
    else:
        return(imDest)






######### 
######### 
######### Method 1
######### 
######### 
######### 







imDest = Image.new("RGB", im.size) #can add "white as 3rd argument to define background color"

### Cropping a piece of the original image

#box = (50, 50, 200, 200)
# imDest = crop_and_paste(im, imDest, (50, 50, 200, 200), random.gauss(1,sigma_brightness), random.gauss(1,sigma_contrast))
# imDest = crop_and_paste(im, imDest, (150, 150, 300, 300), random.gauss(1,sigma_brightness), random.gauss(1,sigma_contrast))
# imDest = crop_and_paste(im, imDest, (-2, -2, 60, 75), random.gauss(1,sigma_brightness), random.gauss(1,sigma_contrast))

x_corners = range(0, im.size[0] + 1, im.size[0] / 10)
y_corners = range(0, im.size[1] + 1, im.size[1] / 10)

for i in range(0,len(x_corners)-1):
    for j in range(0,len(y_corners)-1): 
        # thisBox = (
        #     int(x_corners[i] + random.gauss(0,sigma_pixels)), 
        #     int(y_corners[j] + random.gauss(0,sigma_pixels)), 
        #     int(x_corners[i+1] + random.gauss(0,sigma_pixels)), 
        #     int(y_corners[j+1] + random.gauss(0,sigma_pixels))
        #     )
        thisBox = (
            int(x_corners[i] + random.gauss(20,sigma_pixels)), 
            int(y_corners[j] + random.gauss(20,sigma_pixels)), 
            int(x_corners[i+1] + random.gauss(20,sigma_pixels)), 
            int(y_corners[j+1] + random.gauss(20,sigma_pixels))
            )
        # thisBox = (
        #     x_corners[i], 
        #     y_corners[j], 
        #     x_corners[i+1], 
        #     y_corners[j+1]
        #     )
        
        
        
        # thisBox = (
        #     x_corners[i] - 10, 
        #     y_corners[j] - 10, 
        #     x_corners[i+1] + 10, 
        #     y_corners[j+1] + 10
        #     )   
            
        ### Rotating  
        if rotate: 
            angle=random.randrange(0,90)
            width = abs(thisBox[2] - thisBox[0])
            height = abs(thisBox[3] - thisBox[1])
            xcenter = thisBox[0] - (width/2)
            ycenter = thisBox[1] - (height/2)
            
            thisBox2 = (
                int(xcenter + ( width / 2 ) * math.cos(angle) - ( height / 2 ) * math.sin(angle)), 
                int(ycenter + ( height / 2 ) * math.cos(angle)  + ( width / 2 ) * math.sin(angle)), 
                int(xcenter - ( width / 2 ) * math.cos(angle) + ( height / 2 ) * math.sin(angle)) ,  
                int(ycenter - ( height / 2 ) * math.cos(angle)  - ( width / 2 ) * math.sin(angle))     
                )     
         
        print thisBox
        print thisBox2
       
        try:
            if rotate:
                imDest = crop_and_paste(im, imDest, thisBox2, random.gauss(1,sigma_brightness), random.gauss(1,sigma_contrast))
            else:
                imDest = crop_and_paste(im, imDest, thisBox, random.gauss(1,sigma_brightness), random.gauss(1,sigma_contrast))
        except ZeroDivisionError:
            print >> sys.stderr, "Division by zero bypassed."
        
        print "--------"


imDest.save(outdir + "test" + ext)

















######### 
######### 
######### Method 2
######### Slicing image in small pieces and replacing by image of same size and of unique colour
######### 
######### 




im = Image.open(imageFile)


imDest2 = Image.new("RGB", im.size) #can add "white as 3rd argument to define background color"


x_corners = range(0, im.size[0] + 1, im.size[0] / 50) # Might want to set this number as a parameter
y_corners = range(0, im.size[1] + 1, im.size[1] / 30) # Might want to set this number as a parameter
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


imDest2.save(outdir + "test2" + ext)


