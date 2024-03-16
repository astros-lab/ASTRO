import requests
import cm2py as cm2
import json

def get_command(message: str):
    separated = message.split(" ")
    return separated[0], separated[1:]

def dpaste(text):
    data = {"content": text, "syntax": "text", "expiry_days": 1}
    headers = {"User-Agent": "saveString"}
    r = requests.post("https://dpaste.com/api/v2/", data=data, headers=headers)
    raw_url = f"{r.text.strip()}.txt"  
    return raw_url

def make_text(text, step=0.5, format=True):
    save = cm2.Save()

    row = 0
    col = 0
    for c in text:
        ascii_val = ord(c)
        if format == True and ascii_val == 10:
            col = 0
            row += 1
        
        if ascii_val != 10:
            save.addBlock(cm2.TEXT, (col * step, 0, row), properties=[ascii_val], snapToGrid=False)
            col +=1

    saveString = save.exportSave()

    returning = f"{saveString}"

    return returning

def generate_decoder(inputs):
    def possibilites(amount):
        if amount == 0:
            return ['']
        else:
            possibles = []
            for p in possibilites(amount-1):
                possibles.append(p + '0')
                possibles.append(p + '1')
            return possibles

    save = cm2.Save()

    inputGate = []
    nots = []
    ands = []

    for i in range(inputs):
        inputGate.append(save.addBlock(cm2.OR, (-i, 0, 0)))
        nots.append(save.addBlock(cm2.NOR, (-i-inputs, 0, 0)))
        save.addConnection(inputGate[i], nots[i])

    combinations = possibilites(inputs)

    for p in range(len(combinations)):
        ands.append(save.addBlock(cm2.AND, (-p, 0, 1)))

    for a in range(len(combinations)):
        counter = 0
        for b in combinations[a]:
            if int(b) == 0:
                save.addConnection(inputGate[counter], ands[a])
            elif int(b) == 1:
                save.addConnection(nots[counter], ands[a])
            counter += 1

    saveString = save.exportSave()
    return saveString

def json_add(data, path, filename="commands.json"):
    with open(f"{path}{filename}", "r+") as jsonFile:
        file_data = json.load(jsonFile)
        file_data["commands"].append(data)
        jsonFile.seek(0)
        json.dump(file_data, jsonFile, indent=4)

def rgb_hex(r, g, b): #UNUSED
    hex_code = '#' + '{:02x}{:02x}{:02x}'.format(r, g, b)
    return hex_code
