import json

TOTAL_TESTS = 0
DISCREPANT_TESTS = 0

def get_methods_from_file(file_path):

    with open(file_path, "r") as f:
        methods = f.read().splitlines()

    return methods



def find_tests_with_methods(methods_json_path, methods_file_path):
    global DISCREPANT_TESTS
    global TOTAL_TESTS

    methods = get_methods_from_file(methods_file_path)
    
    with open(methods_json_path, "r") as f:
        json_data = json.load(f)

    tests = json_data.keys()

    for i in tests:
        if not json_data[i] == []: # remove tests with no cloud methods
            TOTAL_TESTS += 1

    tests_with_methods = []
    for key, value in json_data.items():
        for method in methods:
            if method in value:
                print(method)
                tests_with_methods.append(key)
                break

    DISCREPANT_TESTS = len(tests_with_methods)

    return tests, tests_with_methods


def sum_methods_if_test_exists(traffic_json_path, discrepant_test_names):
  
    with open(traffic_json_path, "r") as f:
        traffic_data = json.load(f)

    cost = {
        "PUT": 0,
        "GET": 0,
        "POST": 0,
        "DELETE": 0,
        "PATCH": 0,
        "HEAD": 0,
        "OTHER": 0
    }

    for key, value in traffic_data.items():
        
        # run on cloud if discrepant test
        if key in discrepant_test_names:
            for request in cost:
                for key in value.keys():
                    cost[request] += value[key][request]

    return cost


if __name__ == "__main__":

    methods_json_path = "sdk_methods/Orleans.json"
    methods_file_path = "discrepantApisDotNet.txt"
    traffic_json_path = "application_cost_data/orleans.json"

    total_tests, discrepant_tests = find_tests_with_methods(methods_json_path, methods_file_path)

    # print("Test with discrepant methods:")
    # for name in discrepant_tests:
    #     print(name)

    # all tests on the cloud
    total_cost = sum_methods_if_test_exists(traffic_json_path, total_tests)
    print("*CLOUD COST*")
    for i in total_cost:
        print(i, total_cost[i])
    print()

    # a combination of cloud and emulator
    total_cost = sum_methods_if_test_exists(traffic_json_path, discrepant_tests)
    print("*CLOUD & EMULATOR COST*")
    for i in total_cost:
        print(i, total_cost[i])
    print()

    print("Total tests: ", TOTAL_TESTS)
    print("Potential discrepant tests: ", DISCREPANT_TESTS)
