import cv2
from PIL import Image
import os
import cm2py as cm2
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import botcommands

load_dotenv()
NAME = os.environ['name']

def convertvideo(path, fps=10, height=16, tps=2, threshold=128):
    global NAME, currentlyconverting
    start=datetime.now()
    save = cm2.Save()
    frames = {}
    cap = cv2.VideoCapture(path)
    i = 0

    frameskip = fps
    framecount = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if i > frameskip - 1:
            framecount += 1
            cv2.imwrite(f'/home/{NAME}/workspace/ASTRO/frames/videoframe_' + str(framecount) + '.jpg', frame)

            image_file = Image.open(f"/home/{NAME}/workspace/ASTRO/frames/videoframe_{str(framecount)}.jpg")

            xdim, ydim = round(image_file.size[0] / (image_file.size[1] / height)), height

            compressed = image_file.resize((xdim, ydim))
            
            fn = lambda x : 255 if x > threshold else 0
            converted = compressed.convert('L').point(fn, mode='1')

            converted.save(f"/home/{NAME}/workspace/ASTRO/frames/" + 'converted_' + str(framecount) + '.jpg')
            os.remove(f'/home/{NAME}/workspace/ASTRO/frames/videoframe_' + str(framecount) + '.jpg')

            frames[str(framecount)] = []
            im = Image.open(f"/home/{NAME}/workspace/ASTRO/frames/" + 'converted_' + str(framecount) + '.jpg')
            colors = list(im.getdata())
            for x in range(xdim):
                frames[str(framecount)].append([])
                for y in range(ydim):
                    a = colors[y * xdim + x]
                    blackorwhite = round(a / 255)
                    frames[str(framecount)][x].append(blackorwhite)

            os.remove(f"/home/{NAME}/workspace/ASTRO/frames/" + 'converted_' + str(framecount) + '.jpg')

            if str(datetime.now()-start).split(":")[1] == "01":
                os.remove(path)
                return "Took over 1 minute, canceled. Set fps higher to reduce time."

            i = 0
            continue
        i+=1
    
    cap.release()
    cv2.destroyAllWindows()

    flipflops = []

    for x in range(xdim):
        flipflops.append([])
        for y in range(ydim):
            flipflops[x].append(save.addBlock(cm2.FLIPFLOP, (x, 0, y)))
            y += 1
        x += 1

    frame_blocks = []

    for f in range(len(frames.keys())):
        frame_blocks.append(save.addBlock(cm2.DELAY, (-1, 0 , f), properties=[tps]))
        if len(frame_blocks) != 1:
            save.addConnection(frame_blocks[f-1], frame_blocks[f])
        for x in range(len(frames[str(f+1)])):
            for y in range(len(frames[str(f+1)][x])):
                if f == 0 and frames[str(f+1)][x][y] == 1:
                    save.addConnection(frame_blocks[f], flipflops[x][y])
                elif f != 0 and frames[str(f)][x][y] != frames[str(f+1)][x][y]:
                    save.addConnection(frame_blocks[f], flipflops[x][y])

    resetblock = save.addBlock(cm2.DELAY, (-1, 0, len(frames.keys())), properties=[tps])
    frame_blocks.append(resetblock)
    save.addConnection(frame_blocks[-2], frame_blocks[-1])

    for x in range(len(frames[str(f+1)])):
        for y in range(len(frames[str(f+1)][x])):
            if frames[str(len(frames))][x][y] == 1:
                save.addConnection(frame_blocks[len(frames)], flipflops[x][y])

    saveString = save.exportSave()

    url = botcommands.dpaste(saveString)
    os.remove(path)
    return f"Here's the result! ({datetime.now()-start}):\n\n**File**: {path.split('/')[-1]}```\n{url}```\n**FPS**: {fps} **TPS**: {tps}\n**Dimensions**: {xdim}, {ydim}\n**Threshold**: {threshold}"
