import json
import os
import argparse

def combine_messages(dir):
    # dir = "inbox"
    all_folders = os.listdir(dir)
    for folder in all_folders:
        if dir.startswith("."): # borrowed Mac fix
            continue
        all_files = os.listdir(dir + "/" + folder)
        if "message.json" in all_files:
            continue # skip if message.json exists
        dirs = [dir for dir in all_files if dir.startswith("message")] # filter out other files
        combined = json.loads(open(dir + "/" + folder + "/" + dirs[0], 'r').read())
        dirs.remove(dirs[0])
        for dir0 in dirs:
            json_dir = json.loads(open(dir + "/" + folder + "/" + dir0, 'r').read())
            combined["messages"] = combined["messages"] + json_dir["messages"]
        with open(dir + "/" + folder + '/message.json', 'w') as fp:
            json.dump(combined, fp)
        print("Finished folder " + folder + ", total # of files: " + str(len(combined["messages"])))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Utility for combining messages jsons')
    parser.add_argument(
        '--dir', help="Root folder that contains all the individual messages folders (currently inbox)", required=True)
    args = parser.parse_args()

    base_dir = args.dir
    combine_messages(base_dir)