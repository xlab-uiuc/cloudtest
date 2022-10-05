# Do everything OFFLINE
from http.client import HTTPResponse
import os
import json
import argparse
import re
from utils import find_latest_dir, get_index_of_closing_bracket


def api_files_generator(result_dir_str, is_put=False):
    stat_directory = os.fsencode(result_dir_str)
    # Test name as dir name
    for test_dir in os.listdir(stat_directory):
        test_dir_name = os.fsdecode(test_dir)
        test_dir_str = os.path.join(result_dir_str, test_dir_name)
        if os.path.isdir(test_dir_str):
            # Test round name as dir name, e.g., 0
            for test_round_dir in os.listdir(test_dir_str):
                test_round_dir_str = os.path.join(test_dir_str, test_round_dir)
                # print(test_round_dir_str)
                for stat_file in os.listdir(test_round_dir_str):
                    # stat_file_name = os.fsencode(stat_file)
                    # print(stat_file)
                    if stat_file == "request.json":
                        request_path = os.path.join(test_round_dir_str, stat_file)
                        if os.path.getsize(request_path) > 0:
                            req_file = open(request_path)
                            # # Parse PUT json file which contains multiple json arrays
                            if is_put == True:
                                json_string = req_file.readlines()[0]
                                pattern = '^\[\]'
                                result = re.match(pattern, json_string)
                                if result:
                                    req_file.close()
                                    continue
                                index_cb = get_index_of_closing_bracket(json_string, 0)
                                json_string = json_string[:index_cb+1]
                                data = json.loads(json_string)
                            else:                        
                                data = json.load(req_file)
                            
                            # Beautify the json file
                            with open(os.path.join(test_round_dir_str, "b_request.json"), "w") as f:
                                f.write(json.dumps(data, sort_keys=True, indent=4))
                            # print("test_round_dir_str = " + test_round_dir_str )



if __name__ == "__main__":

    def_directory = find_latest_dir(os.path.join(os.getcwd(), "stat"))
    # def_directory = "stat/Orleans_2022.09.11.17.33.30"
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default = def_directory, help="The directory to run analysis")
    parser.add_argument("-u", "--put_flag", default = False, help="Parameterized unit test flag")
    args = parser.parse_args()
    if args.dir != def_directory:
        tar_dir = os.path.join(os.getcwd(), "stat") +"/" + args.dir
    else:
        tar_dir = args.dir

    api_files_generator(tar_dir, args.put_flag)
