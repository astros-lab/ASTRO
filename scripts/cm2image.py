import cm2py as cm2
from PIL import Image
import math
import requests
from datetime import datetime
import botcommands

def convert_image(sentimage, maxsize, spacingfactor, sender):
    if maxsize > 500_000 and str(sender) != "gaming4cats":
        return "Max raw size must be under 500k raw."
    if spacingfactor > 20 and str(sender) != "gaming4cats":
        return "Spacing factor recommened to be under 20."

    start=datetime.now()

    try:
        image = Image.open(sentimage)
    except:
        return "Error opening file."
    
    # File Size Estimation
    maxpixels = maxsize / 23
    imagesize = image.width * image.height
    ratio = math.floor(math.sqrt(imagesize / maxpixels))

    counter = ratio
    if counter == 0: counter += 1

    underKb = False
    while underKb == False:
        save = cm2.Save()

        reducedimage = image.reduce(counter)
        colors = list(reducedimage.getdata())
        dimensions = reducedimage.size

        estimatedsize = dimensions[0] * dimensions[1] * 23
        if estimatedsize >= maxsize:
            counter += 1
            continue

        for x in range(dimensions[0]):
            for height in range(dimensions[1]):
                color_vars = colors[height * dimensions[0] + x]
                y = dimensions[1] - 1 - height
                spacing = 1 / spacingfactor
                z = x * y * 0.00001
                if isinstance(color_vars, int):
                    save.addBlock(cm2.TILE, (x * spacing, y * spacing, z), properties=[color_vars, color_vars, color_vars], snapToGrid=False)
                else:
                    save.addBlock(cm2.TILE, (x * spacing, y * spacing, z), properties=[color_vars[0], color_vars[1], color_vars[2]], snapToGrid=False)

        saveString = save.exportSave()      
        saveLength = len(saveString)

        if saveLength <= maxsize:
            underKb = True
        else: counter += 1

    raw_url = botcommands.dpaste(saveString)
    return f"Here's the result! ({datetime.now()-start}):\n```{raw_url}```"
