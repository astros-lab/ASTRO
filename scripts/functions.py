import requests
import cm2py as cm2

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
