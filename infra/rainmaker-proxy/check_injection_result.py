from enum import unique
from inspect import trace
from urllib import response
import xml.etree.ElementTree as ET
import os
import glob
import json
import argparse
import pandas
import csv
from bug_inspection_creator import generate_reproduction_file
from utils import return_latest_dir_name

output_dir = os.path.join("alarms")
os.makedirs(output_dir, exist_ok=True)

descp = "This is bug inspection file generator"

# def_round = "storage-injection-round_2022.07.30.14.59.00"
# def_round = "\stat\"

# def_round = return_latest_dir_name("stat")
# def_round = "fhir-server-injection-round_2022.08.15.09.50.01"
# def_round = "storage-injection-round_2022.08.21.22.10.13"
# def_round = "storage-injection-round_2022.08.21.16.47.01"
# def_round = "sleet-injection-round_2022.08.23.00.56.56"
# def_round = "storage-injection-round_2022.08.22.13.30.52"
# def_round = "efcore-injection-round_2022.08.25.12.55.51 "
# def_round = "Insights-injection-round-request-block_2022.06.13.15.52.16"

# def_proj = "Alpakka"
# def_policy = "timeout_first_then_req"
# def_round = "Alpakka-injection-round_2022.09.14.11.58.08"
# def_vanilla_round = "Alpakka_2022.09.13.23.43.12"

# def_proj = "IronPigeon"
# def_policy = "timeout_first_then_req"
# def_round = "IronPigeon-injection-round_2022.09.13.23.26.21"
# def_vanilla_round = "IronPigeon_2022.09.13.22.07.03"

# def_proj = "sleet"
# def_policy = "timeout_first_then_req"
# def_round = "sleet-injection-round_2022.08.23.12.43.34"
# def_vanilla_round = "sleet_2022.07.25.11.54.00"

# azure
# def_proj = "storage"
# def_policy = "timeout_first_then_req"
# def_round = "storage-injection-round_2022.09.16.14.00.25"
# def_vanilla_round = "storage-aws_2022.07.18.13.57.02"


def_proj = "insights"
def_policy = "request_block"
def_round = "Insights-injection-round-request-block_2022.06.13.15.52.16"
def_vanilla_round = "Insights_2022.06.12.18.16.23"

# def_round = "Orleans_2022.08.18.15.00.35"
# def_round = "Botbuilder-dotnet-injection-round_2022.08.24.02.50.35"
# def_round = return_latest_dir_name("stat")
# def_round = "Insights-injection-round-blind-all_2022.08.24.10.24.16"

# def_round = "storage-injection-round-Aws-request_2022.07.18.23.25.11"
# def_vanilla_round = "storage_2022.07.18.13.57.02"
# def_round = "storage-injection-round_2022.07.22.00.38.34"
# def_vanilla_round = "sleet_2022.07.25.11.54.00"
# def_round = "sleet-injection-round_2022.07.25.12.07.33"

# def_directory = "../../results/Botbuilder-dotnet_2022.05.06.06.00.32"
# def_request = "Botbuilder-dotnet-injection-round-500timeout_2022.05.06.06.33.24"
# def_response = "Botbuilder-dotnet-injection-round-503Req_2022.05.09.07.09.34"

# BotBuilder
# def_round = "Botbuilder-dotnet-injection-round-500timeout_2022.05.06.06.33.24"
# def_round = "Botbuilder-dotnet-injection-round-503Req_2022.05.09.07.09.34"
# def_round = "Botbuilder-dotnet-injection-round_2022.08.24.02.50.35"
# def_round = "Botbuilder-dotnet-injection-round_2022.08.31.20.53.09"
# def_vanilla_round = "Botbuilder-dotnet_2022.05.06.06.00.32"
# def_proj = "botbuilder-dotnet"
# def_policy = "timeout_injection"
# keep_boring

# For DistributedLock
# def_round = "DistributedLock-injection-round_2022.08.19.20.53.36"
# def_vanilla_round = "DistributedLock_2022.05.13.05.29.54"
# def_proj = "distributedlock"
# def_policy = "timeout_first_request_block"

# proj = "distributedlock"
# raw_stat_directory = "DistributedLock_2022.05.13.05.29.54"
# stat_directory = "DistributedLock_2022.05.13.05.29.54"
# outcome_directory = "DistributedLock_2022.05.13.05.29.54"
# stat_directory = "DistributedLock-injection-round_2022.05.13.14.59.00"
# stat_directory = "DistributedLock-injection-round_2022.05.14.21.16.36"
# stat_directory = "DistributedLock-injection-round_2022.08.18.23.03.07"
# stat_directory = "DistributedLock-injection-round_2022.08.19.20.53.36"

# def_round = "Insights-injection-round-1st-request_2022.08.24.15.34.03"
# def_vanilla_round = "storage-aws_2022.07.18.13.57.02"
# def_vanilla_round = "servicestack_2022.07.19.20.50.26"
# def_vanilla_round = "efcore_2022.08.04.20.55.22"
# def_vanilla_round = "fhir-server_2022.08.14.03.09.23"
# def_vanilla_round = "storage-aws_2022.07.18.13.57.02"
# def_vanilla_round = "Orleans_2022.08.18.15.00.35"
# def_round = "servicestack-injection-round_2022.07.25.15.25.04"

# def_vanilla_round = "Insights_2022.08.24.09.54.57"
# def_proj = "insights"
# def_proj = "orleans"
# def_policy = "keep_boring"
# def_policy = "timeout_blind_all"
# def_policy = "request_block"
# def_policy = "timeout_first_request_block"
# timeout_injection
# request_block
# timeout_blind_all

# def_vanilla_round = "Insights_2022.08.24.09.54.57"
# def_vanilla_round = "Orleans_2022.08.18.15.00.35"
# def_round = "servicestack-injection-round_2022.07.25.15.25.04"
# def_vanilla_round = "storage_2022.08.21.14.26.12"
# def_vanilla_round = "Insights_2022.06.12.18.16.23"

# def_proj = "storage"
# def_policy = "timeout_blind_all"
# def_proj = "Insights"
# def_proj = "Orleans"
# def_policy = "timeout_injection"
# timeout_injection
# request_block
# def_cloudservice = "AzureStorage"
def_cloudservice = "AzureStorage"
parser = argparse.ArgumentParser(
    description=descp, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--round", "-r", default=def_round,
                    help="The injection round (normally should be the latest one with timestamp)")
parser.add_argument("--vanilla", "-v", default=def_vanilla_round,
                    help="The vanilla round without any injection")
parser.add_argument("--project", "-p", default=def_proj,
                    help="The project name")
parser.add_argument("--policy", "-P", default=def_policy,
                    help="The policy used for injection")
parser.add_argument("--CloudService","-c",default= def_cloudservice,
                    help="The cloud service we used for injection")

args = parser.parse_args()

# result_dir = "outcome/Orleans-injection-round_2022.02.25.20.31.34"
# stat_dir = "stat/Orleans-injection-round_2022.02.25.20.31.34"
# result_dir = "outcome/Orleans-injection-round_2022.03.09.18.39.46"
# stat_dir = "stat/Orleans-injection-round_2022.03.09.18.39.46"
# result_dir = "outcome/Orleans-injection-round_2022.03.11.05.35.34"
# stat_dir = "stat/Orleans-injection-round_2022.03.11.05.35.34"
result_dir = os.path.join("outcome", args.round)   #outcome/
stat_dir = os.path.join("stat", args.round)        #stat/

if args.CloudService == "AzureStorage":
    retry_aware = True
else:
    retry_aware = False

exceptions_to_ignore = {
    "keep_boring":[

    ],
    "request_block": [
        "Microsoft.Azure.Storage.StorageException : Service Unavailable",
        "Microsoft.WindowsAzure.Storage.StorageException : Service Unavailable",
        "Microsoft.WindowsAzure.Storage.StorageException : Fiddled",
        "Microsoft.Azure.Storage.StorageException : Fiddled",
        "Microsoft.WindowsAzure.Storage.StorageException: The remote server returned an error: (503) Server Unavailable.",
        "Azure.RequestFailedException : The server is busy..",
        "Status: 503 (Fiddled)",
        "Status: 503 (Service Unavailable)",
        "System.Xml.XmlException : Data at the root level is invalid",
        "System.Xml.XmlException : Root element is missing.",
        "System.Xml.XmlException: Root element is missing.",
        "Microsoft.Azure.Documents.DocumentClientException : <?xml version=\"1.0\" encoding=\"utf-8\"?><Error><Code>ServerBusy</Code><Message>The server is busy..",
        "Microsoft.Azure.Cosmos.CosmosException : Response status code does not indicate success: ServiceUnavailable (503);",
        "Amazon.S3.AmazonS3Exception : Error making request with Error Code ServiceUnavailable",
    ],
    "timeout_injection": [
        "Status: 500",
        "System.Xml.XmlException : Data at the root level is invalid",
        "System.Xml.XmlException : Root element is missing.",
        "System.Xml.XmlException: Root element is missing.",
        # "Microsoft.Azure.Cosmos.CosmosException : Response status code does not indicate success: ServiceUnavailable (503)",
        "System.ArgumentNullException",
        '"StatusCode":"ServiceUnavailable"',
        "System.Net.Http.HttpRequestException : Response status code does not indicate success:",
        "System.TimeoutException : The operation was canceled.",
    ],
    "delay_injection": [],
    "timeout_blind_all":[
        "Status: 500",
        " Http Status Code InternalServerError. No further error information was returned by the service.",
        "System.Xml.XmlException : Data at the root level is invalid",
        "System.Xml.XmlException : Root element is missing.",
        "System.Xml.XmlException: Root element is missing.",
        "Amazon.S3.AmazonS3Exception : Error making request with Error Code ServiceUnavailable",
        "Error Code ServiceUnavailable",
        "Amazon.S3.AmazonS3Exception : Error making request with Error Code ServiceUnavailable",
        "Amazon.S3.AmazonS3Exception : Error making request with Error Code InternalServerError",
        "System.TimeoutException : The operation was canceled.",
        " System.Net.Sockets.SocketException : The I/O operation has been aborted because of either a thread exit or an application request",
    ],
    "timeout_first_request_block":[
        "Status: 500",
        "ServiceUnavailable",
        "System.Net.Http.HttpRequestException : Response status code does not indicate success: 500",
        "Microsoft.Azure.Storage.StorageException : Service Unavailable",
        "Microsoft.WindowsAzure.Storage.StorageException : Service Unavailable",
        "Microsoft.WindowsAzure.Storage.StorageException : Fiddled",
        "Microsoft.Azure.Storage.StorageException : Fiddled",
        "Microsoft.WindowsAzure.Storage.StorageException: The remote server returned an error: (503) Server Unavailable.",
        "Azure.RequestFailedException : The server is busy..",
        "Status: 503 (Fiddled)",
        "Status: 503 (Service Unavailable)",
        "System.Xml.XmlException : Data at the root level is invalid",
        "System.Xml.XmlException : Root element is missing.",
        "System.Xml.XmlException: Root element is missing.",
        "Microsoft.Azure.Documents.DocumentClientException : <?xml version=\"1.0\" encoding=\"utf-8\"?><Error><Code>ServerBusy</Code><Message>The server is busy..",
        "Microsoft.Azure.Cosmos.CosmosException : Response status code does not indicate success: ServiceUnavailable (503);",
        "Amazon.S3.AmazonS3Exception : Error making request with Error Code ServiceUnavailable"
    ]
}

cloud_service_namespace = [
    "Azure.Core.",
    "Azure.Storage."
]


xmlns = "{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}"


def inspect_test_failure(test_result_file, policy, retry_flag):
    if retry_flag:
        json_file_location = "stat" + test_result_file[7:]
        json_turn = json_file_location[-7]
        # print("Test Json Turn = " + json_turn)
        json_file_location = json_file_location.rsplit("\\",1)[0] + "\\" + json_turn + "\\b_request.json"
        # print("Test Stat Json location" + json_file_location)
        with open(json_file_location) as f:
            b_json_file = json.load(f)
        inject_flag = False
    
        cnt_500 = 0
        cnt_503 = 0
        for j_ele in b_json_file:
            if ('httpResponse' in j_ele) and ('headers' in j_ele['httpResponse']) and ('injected' in j_ele['httpResponse']['headers']):
                inject_flag = True
                tmp_status_code = j_ele['httpResponse']['statusCode']
                if tmp_status_code == 503:
                    cnt_503 += 1
                elif tmp_status_code == 500:
                    cnt_500 += 1

    # print(j_ele['httpResponse']['headers'].keys())
    # print("enter inspection")
    tree = ET.parse(test_result_file)
    root = tree.getroot()
    test_pass = False
    boring_failure = False
    fail_in_test = False
    results_field = root.find(xmlns + 'Results')  # .attrib.get('outcome')
    # if "Microsoft.EntityFrameworkCore.Cosmos.OptimisticConcurrencyCosmosTest.Simple_concurrency_exception_can_be_resolved_with_store_values" in test_result_file:
    #     print(test_result_file)
    if len(list(root.iter(xmlns + "ErrorInfo"))) == 0 and results_field is not None:
        test_pass = True
        # print("ErrorInfo length is 0")
        return test_pass, boring_failure, fail_in_test, ""
    resultsum = root.find(xmlns + 'ResultSummary')
    if results_field is None and resultsum.attrib.get('outcome') == "Failed":
        print("Test result field is None (blamed test): {}".format(test_result_file))
        run_info = list(root.iter(xmlns + "RunInfo"))[0]
        blamed_text = run_info.find(xmlns + "Text").text.split("\n")[0]
        return test_pass, boring_failure, fail_in_test, blamed_text.strip().replace(
            "\n", " ").replace("\r", " ").replace("\t", " ")
    # print(test_result_file)
    result_sum_info = list(root.iter(xmlns + "ResultSummary"))[0]
    if results_field is None and result_sum_info.find(xmlns + "Counters").attrib.get('total') == "0":
        boring_failure = True
        return test_pass, boring_failure, fail_in_test, "Cannot find test"
    error_info = list(root.iter(xmlns + "ErrorInfo"))[0]
    message = error_info.find(xmlns + "Message")
    stacktrace = error_info.find(xmlns + "StackTrace")
    # print(message.text)
    for ele in exceptions_to_ignore[policy]:
        # print(ele)
        if ele in message.text:
            if(retry_flag):
                if (cnt_503 <= 1) and (cnt_500 <= 1) and inject_flag:
                    print("Trivial pattern")
                    boring_failure = False
                else:
                    boring_failure = True
                    return test_pass, boring_failure, fail_in_test, ""
            else:
                boring_failure = True
                return test_pass, boring_failure, fail_in_test, ""
    if stacktrace is not None:
        if stacktrace.text is not None:
            traces = stacktrace.text.split("\n")
            if "\\test" in traces[0] or\
                "test" in traces[0] or\
                "Test" in traces[0]:
                # print(traces[0])
                fail_in_test = True
            # else:
            #     print("Trace does not contain test keyword")
        else:
            # print("Test for bug_inspection.csv")
            print(test_result_file)
            print(stacktrace)
    else:
        print("stacktrace is None")

    return test_pass, boring_failure, fail_in_test, message.text.strip().replace(
        "\n", " ").replace("\r", " ").replace("\t", " ")


def check(test_result_files, test_dll, test_policy):
    f = open(os.path.join(output_dir, "{}-{}.tsv".format(test_dll, test_policy)), "w", encoding="utf-8")
    f.write("name\tpolicy\tround\toutcome\tmessage\tfail_in_test\tboring_failure\n")
    test_run_cnt = len(test_result_files)
    test_failure_cnt = test_run_cnt
    interesting_test_failure_cnt = test_run_cnt
    alarms_cnt = test_run_cnt
    fail_in_test_cnt = 0
    transformed_exception_test_cnt = 0

    assertion_cat = 0
    exception_types = dict()
    failed_test_cnt = 0

    host_crash_cnt = 0

    for test_result_file in test_result_files:
        test_pass, boring_failure, fail_in_test, plain_message = inspect_test_failure(
            test_result_file, test_policy, retry_aware)
        if test_pass:
            test_failure_cnt -= 1
            interesting_test_failure_cnt -= 1
            alarms_cnt -= 1
            test_outcome = "Passed"
            continue
        elif (boring_failure and args.policy != "keep_boring"):
            transformed_exception_test_cnt += 1
            interesting_test_failure_cnt -= 1
            alarms_cnt -= 1
            test_outcome = "Failed"
            # if args.policy == "request_block":
            #     continue
            # justify the unit test oracle 
            continue
        elif fail_in_test:
            alarms_cnt -= 1
            fail_in_test_cnt += 1
            test_outcome = "Failed"
            continue
        else:
            test_outcome = "Failed"
            # justify the unit test oracle
            # continue
        test_dll, test_name, test_policy, test_round, _ = tear_down_path(test_result_file)

        failed_test_cnt += 1
        if "Assert." in plain_message or "Expected: " in plain_message:
            assertion_cat += 1
        elif "Exception :" in plain_message:
            exception_type = plain_message.split(" :")[0]
            if exception_type in exception_types:
                exception_types[exception_type] += 1
            else:
                exception_types[exception_type] = 1
        elif "Exception:" in plain_message:
            # print(plain_message)
            exception_type = plain_message.split("Exception:")[0].split(". ")[-1]
            if exception_type in exception_types:
                exception_types[exception_type + "Exception"] += 1
            else:
                exception_types[exception_type + "Exception"] = 1
        elif "The active test run was aborted. Reason: Test host process crashed" in plain_message:
            host_crash_cnt += 1
        else:
            print(plain_message)

        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            test_name, test_policy, test_round, test_outcome, plain_message, fail_in_test, boring_failure))
    f.close()
    print("***************************************")
    print("# Total test run: {}".format(test_run_cnt))
    print("# Total test failures: {}".format(test_failure_cnt))
    print("# Failed test we care/interested in (written to csv file): {}".format(failed_test_cnt))
    print("# Test throwing exception from production code: {}".format(alarms_cnt))
    print("# Test throwing exception from test code (e.g., assertion failure or blamed tests): {}".format(fail_in_test_cnt))
    print("# Test throwing non-transformed exception (i.e., boring failure we skip): {}".format(transformed_exception_test_cnt))
    print("# Assertion failure: {}".format(assertion_cat))
    total_excp_cnt = 0
    for key in exception_types:
        total_excp_cnt += exception_types[key]
    print("# Total exception (excluding assertions): {}\nDistribution of exception types: {}".format(total_excp_cnt, exception_types))
    # print("total number of test run: {}\nnumber of test failures: {}\ninteresting failure number: {}\nalarm from production code number: {}"
    #       .format(test_run_cnt, test_failure_cnt, interesting_test_failure_cnt, alarms_cnt))
    print("***************************************")


def tear_down_path(test_result_file):
    # print(test_result_file)
    test_path, test_file = os.path.split(test_result_file)[0], os.path.split(test_result_file)[1]
    test_name = os.path.split(test_path)[1]
    # print(test_file)
    if test_file.split('-')[0] == '0':
        test_round = test_file.split('-')[4]
        test_result = test_file.split('-')[1]
    elif test_file.split('-')[1] == "skipped":
        test_round = test_file.split('-')[4]
        test_result = test_file.split('-')[1]
    else:
        test_round = test_file.split('-')[2]
        test_result = "passed"
    
    return args.project, test_name, args.policy, test_round, test_result


def categorize(result_dir):
    categories_map = {}
    test_result_files = glob.glob(
        os.path.join(result_dir, "**", "*.trx"), recursive=True)
    for test_result_file in test_result_files:
        # print(test_result_file)
        test_dll, test_name, test_policy, test_round, _ = tear_down_path(
            test_result_file)
        # print("测试 = " + test_policy)
        if test_dll not in categories_map:
            categories_map[test_dll] = {}
        if test_policy not in categories_map[test_dll]:
            categories_map[test_dll][test_policy] = []
        categories_map[test_dll][test_policy].append(test_result_file)
    # print(categories_map)
    for test_dll in categories_map.keys():
        for test_policy in categories_map[test_dll].keys():
            check(categories_map[test_dll][test_policy], test_dll, test_policy)

def remove_duplicated(bug_inspection_dir, stacktrace_dir, boring_result = False):
    
    if(boring_result):
        bug_file = os.path.join(bug_inspection_dir,"Boring_failures.csv")
        tmp_bug_file = os.path.join(bug_inspection_dir,"Boring_Unique_test_name.csv")
    else:
        bug_file = os.path.join(bug_inspection_dir,"bug_inspection.csv")
        tmp_bug_file = os.path.join(bug_inspection_dir,"unique_bug_inspection.csv")
    stacktrace_folder = stacktrace_dir
    # assign dataset
    csvData = pandas.read_csv(bug_file,sep='\t')
                               
    # sort data frame
    csvData.sort_values(["SDK"], 
                    axis=0,
                    ascending=[False], 
                    inplace=True)
  
    # displaying sorted data frame
    # print("\nAfter sorting:")
    # print(csvData)
    csvData.to_csv(bug_file,sep='\t', index=False)
    # os.replace(tmp_bug_file, bug_file)
    f = open(tmp_bug_file, "w", encoding="utf-8")

    f.write("name\tturn\tSDK\tpolicy\toutcome\ttime\texcp_type\theuristic1\theuristic2\tURI\tbug?\tbug_ID\tbug_link\n")
    with open(bug_file, newline='') as check_result:
        rows = csv.DictReader(check_result, delimiter='\t')
        tmp_test_name = ""
        tmp_test_turn = ""
        tmp_test_sdk = ""
        sdk_trace = {}
        for row in rows:
            test_name = row['name']
            test_turn = row['turn']
            injected_request = row['URI']
            sdk_api = row['SDK']
            policy = row['policy']
            outcome = row['outcome']
            run_time = row['time']
            excp_type = row['excp_type']
            heur_1 = row['heuristic1']
            heur_2 = row['heuristic2']
            if(tmp_test_sdk != sdk_api):
                tmp_test_sdk = sdk_api
                tmp_test_name = test_name
                tmp_test_turn = test_turn
                dir1 = os.path.join(stacktrace_folder,tmp_test_name) + "/0-failed-test-result-"+str(tmp_test_turn)+"-0.trx"
                sdk_trace.setdefault(sdk_api, [])
                stack_trace = get_stack_trace(dir1)
                if stack_trace != []:
                    sdk_trace[sdk_api].append(stack_trace)
                f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                test_name, test_turn, sdk_api, policy, outcome, run_time, excp_type, heur_1, heur_2, injected_request))
            else:
                dir2 = os.path.join(stacktrace_folder,test_name) + "/0-failed-test-result-"+str(test_turn)+"-0.trx"
                stack_trace = get_stack_trace(dir2)
                if sdk_trace.get(sdk_api, False) != False:
                    if stack_trace in sdk_trace.get(sdk_api):
                        continue
                    else:
                        if stack_trace != []:
                            sdk_trace[sdk_api].append(stack_trace)
                        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                test_name, test_turn, sdk_api, policy, outcome, run_time, excp_type, heur_1, heur_2, injected_request))
                else:
                    sdk_trace.setdefault(sdk_api, [])
                    f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                test_name, test_turn, sdk_api, policy, outcome, run_time, excp_type, heur_1, heur_2, injected_request))
    # print(sdk_trace)
    f.close()

# def compare_stack_trace(dir_1, dir_2):
# def compare_stack_trace(dir1, dir2):
#     tree_1 = ET.parse(dir1)
#     root_1 = tree_1.getroot()
#     error_info_1 = list(root_1.iter(xmlns + "ErrorInfo"))[0]
#     stacktrace_1 = error_info_1.find(xmlns + "StackTrace")
#     trace_1 = []
#     if stacktrace_1 is not None:
#         if stacktrace_1.text is not None:
#             # print(stacktrace.text)
#             trace_1 = stacktrace_1.text.split("\n")
#             trace_1 = [item for item in trace_1 if "\\test\\" not in item]
    
#     tree_2 = ET.parse(dir2)
#     root_2 = tree_2.getroot()
#     error_info_2 = list(root_2.iter(xmlns + "ErrorInfo"))[0]
#     stacktrace_2 = error_info_2.find(xmlns + "StackTrace")
#     trace_2 = []
#     if stacktrace_2 is not None:
#         if stacktrace_2.text is not None:
#             # print(stacktrace.text)
#             trace_2 = stacktrace_2.text.split("\n")
#             trace_2 = [item for item in trace_2 if "\\test\\" not in item]

#     return ( (trace_1 == trace_2), (trace_1,trace_2) )


def get_stack_trace(dir):
    try:    
        tree = ET.parse(dir)
    except:
        trace = []
        return trace
    root = tree.getroot()
    error_info = list(root.iter(xmlns + "ErrorInfo"))[0]
    stacktrace = error_info.find(xmlns + "StackTrace")
    trace = []
    if stacktrace is not None:
        if stacktrace.text is not None:
            # print(stacktrace.text)
            trace = stacktrace.text.split("\n")
            new_trace = []
            for item in trace:
                if "\\test\\" not in item and \
                    "test" not in item and \
                    "Test" not in item:
                    new_trace.append(item)
            # trace = [item for item in trace if "\\test\\" not in item or\
            #     "test" not in item or\
            #     "Test" not in item]

    return new_trace 
def remove_true(output_dir_proj):
    bug_inspection_dir = output_dir_proj
    boring_fails = os.path.join(bug_inspection_dir,"Boring_failures.csv")
    Boring_Unique_test_name = os.path.join(bug_inspection_dir,"Boring_Unique_test_name.csv")
    bug_file = os.path.join(bug_inspection_dir,"bug_inspection.csv")
    tmp_file = os.path.join(bug_inspection_dir,"tmp.csv")
    
    true_rows = []
    boring_rows = []
    boring_tests = []
    with open(bug_file, newline='') as check_result:
        rows = csv.DictReader(check_result, delimiter='\t')
        for row in rows:
            test_name = row['name']
            test_turn = row['turn']
            row_string = "{}\t{}\n".format(
                test_name, test_turn)
            true_rows.append(row_string)
    with open(boring_fails, newline='') as check_result:
        rows = csv.DictReader(check_result, delimiter='\t')
        for row in rows:
            test_name = row['name']
            test_turn = row['turn']
            injected_request = row['URI']
            sdk_api = row['SDK']
            policy = row['policy']
            outcome = row['outcome']
            run_time = row['time']
            excp_type = row['excp_type']
            heur_1 = row['heuristic1']
            heur_2 = row['heuristic2']
            row_string = row_string = "{}\t{}\n".format(test_name, test_turn)
            
            #  "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
            #     test_name, test_turn, sdk_api, policy, outcome, run_time, excp_type, heur_1, heur_2, injected_request)
            if row_string in true_rows:
                continue
            else:
                boring_rows.append(row)
                if row_string not in boring_tests:
                    boring_tests.append(row_string)

    # print("-----------------------")
    # print(len(true_rows))
    # print("-----------------------")
    # print(boring_rows)
    f = open(Boring_Unique_test_name, "w", encoding="utf-8")
    f.write("name\tturn\n")
    for i in boring_tests:
        f.write(i)
    f.close()

    f = open(tmp_file, "w", encoding="utf-8")
    f.write("name\tturn\tSDK\tpolicy\toutcome\ttime\texcp_type\theuristic1\theuristic2\tURI\tbug?\tbug_ID\tbug_link\n")
    for row in boring_rows:
        test_name = row['name']
        test_turn = row['turn']
        injected_request = row['URI']
        sdk_api = row['SDK']
        policy = row['policy']
        outcome = row['outcome']
        run_time = row['time']
        excp_type = row['excp_type']
        heur_1 = row['heuristic1']
        heur_2 = row['heuristic2']
        f.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                test_name, test_turn, sdk_api, policy, outcome, run_time, excp_type, heur_1, heur_2, injected_request))
    # f = open(bug_file, "w", encoding="utf-8")
    f.close()
    os.replace(tmp_file, boring_fails)
    return

if __name__ == "__main__":
    categorize(result_dir)
    if(args.policy == "keep_boring"):
        Def_Boring = True
    else:
        Def_Boring = False
    
    alarm_file_path = os.path.join("alarms", args.project+"-"+args.policy+".tsv")
    inject_stat_round_dir_path = stat_dir
    stat_round_dir_path = os.path.join("stat", args.vanilla)
    stack_dir_path = os.path.join("outcome", args.round)
    output_dir = os.path.join("../../results", args.project)
    output_dir_proj = os.path.join("../../results", args.round)

    generate_reproduction_file(output_dir, output_dir_proj, alarm_file_path, inject_stat_round_dir_path, stat_round_dir_path, Def_Boring)
    remove_duplicated(output_dir_proj, stack_dir_path, Def_Boring)
    if(Def_Boring):
        try:
            remove_true(output_dir_proj)
        except:
            print("Need run other policy first")
