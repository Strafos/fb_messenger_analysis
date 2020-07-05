import json
import os
import argparse

def combine_messages(dir):
    # dir = "inbox"
    all_folders = os.listdir(dir)
    for folder in all_folders:
        current_dir = dir + "/" + folder 
        if folder.startswith("."): # borrowed Mac fix
            continue
        all_files = os.listdir(current_dir)
        if "message.json" in all_files:
            continue # skip if message.json exists
        dirs = [dirt for dirt in all_files if dirt.startswith("message")] # filter out other files
        combined = json.loads(open(current_dir + "/" + dirs[0], 'r').read())
        dirs.remove(dirs[0])
        for dir0 in dirs:
            json_dir = json.loads(open(current_dir + "/" + dir0, 'r').read())
            combined["messages"] = combined["messages"] + json_dir["messages"]
        with open(current_dir + '/message.json', 'w') as fp:
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
