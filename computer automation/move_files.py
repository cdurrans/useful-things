import os
import shutil
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="file folder with files to copy")
    parser.add_argument("--target", help="destination file folder")
    parser.add_argument("--del_target", help="y/n clean destination before transferring")
    parser.add_argument("--del_source", help="y/n clean source folder after transferring")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please specify a target, use --help for more info.")
    elif not args.source:
        parser.error("[-] Please specify a source file folder, use --help for more info.")
    elif not args.del_target:
        parser.error("[-] Please say y/n if you want to delete files in destination folder, use --help for more info.")
    elif not args.del_source:
        parser.error("[-] Please say y/n if you want to delete files in source folder, use --help for more info.")
    return args

args = get_arguments()

def delete_folder(folder):
    for fname in os.listdir(folder):
        try:
            os.remove(os.path.join(folder,fname))
        except PermissionError as ex:
            print(ex)
            pass


if args.del_target[0].lower() == 'y':
    delete_folder(args.target)

for fname in os.listdir(args.source):
    try:
        shutil.copy(os.path.join(args.source, fname), os.path.join(args.target, fname))
    except PermissionError as ex:
        print(ex)
        pass

if args.del_source[0].lower() == 'y':
    delete_folder(args.source)

#example of what it should look like
# python "F:\Shared Folders\Python Scripts\move_files.py" --source "W:/AgentDashboard/" --target "F:/Shared Folders/Agent Dashboard/" --del_target "n" --del_source "y"


# python "F:\Shared Folders\Python Scripts\move_files.py" --source "W:/testSite/BackupsToRestore/" --target "F:/BackUpsToRestore/" --del_target "n" --del_source "y"