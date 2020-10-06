import os

def keepNewestFile(directory, fileStartsWith, newName):
    newestFile = ""
    createdDate = ""
    for fname in os.listdir(directory):
        if fname.startswith(fileStartsWith):
            modTime = os.path.getmtime(os.path.join(directory,fname))
            if createdDate == "":
                createdDate = modTime
                newestFile = fname
            elif createdDate < modTime:
                createdDate = modTime
                os.remove(os.path.join(directory,newestFile))
                print("delete previous new file", newestFile)
                newestFile = fname
            else:
                print('Delete fname because not newer')
                os.remove(os.path.join(directory,fname))
                continue
    os.rename(os.path.join(directory,newestFile), os.path.join(directory,newName))
    print('Renaming ',newestFile,' to ',newName)