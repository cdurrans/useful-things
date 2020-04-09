import os
import shutil
import argparse

#example of what it should look like
# python "F:\Shared Folders\Python Scripts\move_files.py" --source "W:/AgentDashboard/" --target "F:/Shared Folders/Agent Dashboard/"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="file folder with files to copy")
    parser.add_argument("--target", help="destination file folder")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please specify a target, use --help for more info.")
    elif not args.source:
        parser.error("[-] Please specify a source file folder, use --help for more info.")
    return args

args = get_arguments()

for fname in os.listdir(args.source):
    try:
        shutil.copy(args.source + fname, args.target + fname)
    except PermissionError as ex:
        print(ex)
        pass

