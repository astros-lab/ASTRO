import cm2py as cm2
from PIL import Image
import math
import requests
from datetime import datetime

def convert_image(sentimage, maxsize):
    if maxsize > 500000:
        return "Max raw size must be under 500k."

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
            for y in range(dimensions[1]):
                color_vars = colors[y * dimensions[0] + x]
                if isinstance(color_vars, int):
                    save.addBlock(cm2.TILE, (x, dimensions[1] - 1 - y, 0), properties=[color_vars, color_vars, color_vars])
                else:
                    save.addBlock(cm2.TILE, (x, dimensions[1] - 1 - y, 0), properties=[color_vars[0], color_vars[1], color_vars[2]])

        saveString = save.exportSave()      
        saveLength = len(saveString)

        if saveLength <= maxsize:
            underKb = True
        else: counter += 1

    # Sends to dpaste
    data = {"content": saveString, "syntax": "text", "expiry_days": 1}
    headers = {"User-Agent": "saveString"}
    r = requests.post("https://dpaste.com/api/v2/", data=data, headers=headers)
    raw_url = f"{r.text.strip()}.txt"
    return f"Here's the result! ({datetime.now()-start}):\n```{raw_url}```"
