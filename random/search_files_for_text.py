import os 
import shutil

start_directory = 'F:/Shares/GSC-Reporting/PythonScripts/'
search_patterns = ['VDM Live section','VDM','VDM.csv']

for fname in os.listdir(start_directory):
    if fname.endswith('.py'):
        fileExplored = open(os.path.join(start_directory,fname),'r')
        ftext = fileExplored.read()
        fileExplored.close()
        lines = ftext.split('\n')
        for pat in search_patterns:
            for line_idx in range(len(lines)):
                if lines[line_idx].find(pat) > 0:
                    print(f'In {fname}, line {line_idx} is the pattern: {pat}\nContent: {lines[line_idx]}')

        