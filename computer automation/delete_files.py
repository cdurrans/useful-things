#######
#Created 4/9/2020 by Chris Durrans
# Example usage for in a bat file for task scheduler etc.:
#
# call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
#
# python "F:\Shared Folders\Python Scripts\deleteoldFiles.py" --directory "//w13107/GSC-Reporting/SNAndOtherEmailedData/" --days 8 --exclusions ".bat .py .ps1"
#######

import os, time, sys
now = time.time()

import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="file folder with files to delete")
    parser.add_argument("--days", help="Number of days old the files need to be")
    parser.add_argument("--exclusions", help="FileTypesToExclude")
    parser.add_argument("--printMode", help="Do you want to print instead of delete the files in question?")
    args = parser.parse_args()
    if not args.directory:
        parser.error("[-] Please specify a directory, use --help for more info.")
    elif not args.days:
        parser.error("[-] Please specify a days old., use --help for more info.")
    elif not args.exclusions:
        args.exclusions = ' '
    elif not args.printMode:
        args.printMode = False
    return args

args = get_arguments()

exclusions = args.exclusions.split()
print(exclusions)
if args.printMode:
    print('Print mode only enabled. The following are files that would be deleted.')
for fname in os.listdir(args.directory):
    skipFile = False
    for fileType in exclusions:
        if fname.endswith(fileType):
            skipFile = True
    if skipFile == False:
        if os.stat(os.path.join(args.directory, fname)).st_mtime < now - int(args.days) * 86400:
            if args.printMode:
                print(fname)
            else:
                os.remove(os.path.join(args.directory,fname))
                print(fname, 'has been deleted')
    
