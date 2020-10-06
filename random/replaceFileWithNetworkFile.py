import easygui
import os
from pathlib import Path
filePath = easygui.fileopenbox()

def findNetworkLocation(filePath):
    import subprocess
    cmd = "net use"
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout = subprocess.PIPE)
    results = proc.communicate()
    results = str(results[0]).split('\\r')
    for x in results:
        if filePath[:2] in x:
            indx = x.find(filePath[:2])
            fst = x[2+indx:].strip()
            fst = fst.strip()
            fst = fst.split('    ')[0]
    combined = fst.replace('\\\\','\\') + filePath[2:]
    if os.path.isfile(combined):
        return combined
    else:
        return filePath
