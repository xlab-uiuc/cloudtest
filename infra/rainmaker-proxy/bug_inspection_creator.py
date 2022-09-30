import pandas as pd
import csv
import os
import json
import pandas as pd
import re
from utils import get_index_of_closing_bracket

def generate_reproduction_file(output_dir_path, output_dir_proj, alarm_file, stat_round_dir, calibrate_stat_dir, boring_result = False):
    if boring_result:
        bug_f_path = os.path.join(output_dir_path, "Boring_failures.csv")
    else:
        bug_f_path = os.path.join(output_dir_path, "bug_inspection.csv")
    f = open(bug_f_path, "w", encoding="utf-8")
    f.write("name\tturn\tURI\tSDK\tpolicy\toutcome\ttime\texcp_type\theuristic1\theuristic2\tbug?\tbug_ID\tbug_link\n")
    with open(alarm_file, newline='') as injection_result:
        rows = csv.DictReader(injection_result, delimiter='\t')
        marked_test_set = set()
        test_injection_failure = 0
        src_injection_failure = 0
        for row in rows:
            # print(row['name'], row['policy'], row['round'])
            test_name = row['name']
            test_turn = row['round']
              
            try:
                req_f_path, overview_f_path, marked_test, inject_round_num, collect_round_num = locate_files_path(stat_round_dir, calibrate_stat_dir, test_name, test_turn)
            except:
                print("locate_file_path function can not work the test below")
                print("The reason may be that source files are empty")
                print(test_name)
                print(test_turn)
                continue

            if marked_test != "":
                marked_test_set.add((test_name, inject_round_num, collect_round_num))
            injected_request, sdk_api = find_injected_req_and_sdk_api(req_f_path)
            if "Cannot find injected request" in injected_request:
                continue
            policy = row['policy']
            outcome = row['outcome']
            run_time = find_run_time(overview_f_path)
            excp_type = find_excp_type(row['message'])
            heur_1 = selected_by_heuristic_1(row['fail_in_test'])
            heur_2 = selected_by_heuristic_2(row['boring_failure'])
            if "test" in sdk_api:
                test_injection_failure += 1
                continue
            src_injection_failure += 1
            f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                test_name, test_turn, injected_request, sdk_api, policy, outcome, run_time, excp_type, heur_1, heur_2))
    f.close()

    if_dir_exist = os.path.isdir(output_dir_proj)
    if not if_dir_exist:
        os.makedirs(output_dir_proj)
    df_bug = pd.read_csv(bug_f_path, sep='\t')
    # Put the file under full collection folder
    if boring_result:
        df_bug.to_csv(os.path.join(output_dir_proj, "Boring_failures.csv"), sep='\t', index=False)
    else:
        df_bug.to_csv(os.path.join(output_dir_proj, "bug_inspection.csv"), sep='\t', index=False)
    

    print("#######################################")
    print("Number of tests that has inconsistent round number: {}".format(len(marked_test_set)))
    for ele in marked_test_set:
        print("{}; Actual injection #: {}; Expected injection #: {}".format(ele[0], ele[1], ele[2]))
    print("#######################################")
    print("Number of injections on test code: {}".format(test_injection_failure))
    print("Number of injections on source code: {}".format(src_injection_failure))
    print("We prune out injections on test code")
    print("Total failed tests in the bug_inspection: {}".format(src_injection_failure))
    # There are xlocation header with empty values => lead to inconsistent round number
    # print("{}\ntest that has inconsistent round number {}".format(marked_test_set, len(marked_test_set)))


def selected_by_heuristic_1(fail_in_test):
    return "False" if fail_in_test.strip() == "True" else "True"


def selected_by_heuristic_2(boring_failure):
    return "False" if boring_failure.strip() == "True" else "True"


def find_excp_type(plain_message):
    exception_type = "Cannot find exception type"
    if "Assert." in plain_message or "Expected: " in plain_message:
        exception_type = "Assertion"
    elif "Exception :" in plain_message:
        exception_type = plain_message.split(" :")[0]
    elif "Exception:" in plain_message:
        # print(plain_message)
        exception_type = plain_message.split("Exception:")[0].split(". ")[-1]
    return exception_type


def locate_files_path(stat_dir, collection_stat_dir, test_name, injection_round):
    inject_round_num = 0
    inject_test_path = os.path.join(stat_dir, test_name)
    for f in os.listdir(inject_test_path):
        child = os.path.join(inject_test_path, f)
        if os.path.isdir(child):
            inject_round_num += 1
    collect_round_sdk_path = os.path.join(collection_stat_dir, test_name, '0', 'CALLSITE.csv')
    collect_round_num = len(pd.read_csv(collect_round_sdk_path, sep='\t', header=None).index)

    if inject_round_num != collect_round_num:
        marked_test = test_name
    else:
        marked_test = ""

    turn_dir = os.path.join(stat_dir, test_name, injection_round)
    req_f_path = os.path.join(turn_dir, "request.json")
    overview_f_path = os.path.join(turn_dir, "overview.txt")
    return req_f_path, overview_f_path, marked_test, inject_round_num, collect_round_num


def find_injected_req_and_sdk_api(request_file):
    # print(request_file)
    req_file = open(request_file)
    is_put = True
    if is_put == True:
        json_string = req_file.readlines()[0]
        pattern = '^\[\]'
        result = re.match(pattern, json_string)
        if result:
            req_file.close()

        index_cb = get_index_of_closing_bracket(json_string, 0)
        json_string = json_string[:index_cb+1]
        reqs = json.loads(json_string)
    else:                        
        reqs = json.load(req_file)
                            
    # reqs = json.load(req_file)
    uri = "Cannot find injected request"
    sdk_api = "Cannot find SDK API"
    for request in reqs:
        http_request = request['httpRequest']
        http_response = request['httpResponse']
        if "headers" not in http_response:
            continue

        if "injected" in http_response['headers']:
            host = str(http_request['headers']['Host'][0])
            http_method = str(http_request['method'])
            http_path = str(http_request['path'])
            query_string = ""
            if "queryStringParameters" in http_request:
                query_string = "/"
                for key, value in http_request['queryStringParameters'].items():
                    # print(key, value)
                    query_string += key + "=" + value[0]
            uri = host + http_method + http_path + query_string

            if "x-location" in http_request['headers']:
                x_location = http_request['headers']['x-location'][0]
                sdk_api = x_location
                # if "#" in x_location:
                #     sdk_api = x_location.split("#")[-1]
                # else:
                #     sdk_api = x_location
            req_file.close()
            return uri, sdk_api
        else:
            continue
    req_file.close()
    return uri, sdk_api


def find_run_time(overview_file_path):
    overview_file = open(overview_file_path)
    run_time = "Cannot find running time"
    lines = overview_file.readlines()
    for line in lines:
        if line.startswith("Running time"):
            run_time = line.split(":")[1].strip()
            break
    return run_time


# if __name__ == "__main__":
    # Use check_injection_result.py

    # alarm_file_path = os.path.join("alarms", "Tester.AzureUtils.dll-timeout_injection.tsv")
    # inject_stat_round_dir_path = os.path.join("stat", "Orleans-injection-round_2022.03.11.05.35.34")
    # stat_round_dir_path = os.path.join("stat", "Orleans_2022.02.25.00.09.00")
    # project = "orleans"
    # output_dir = os.path.join("../../results", project)
    # generate_reproduction_file(output_dir, alarm_file_path, inject_stat_round_dir_path, stat_round_dir_path)
