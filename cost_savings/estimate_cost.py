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

    tests_with_methods = []
    for key, value in json_data.items():
        for method in methods:
            if method in value:
                tests_with_methods.append(key)

    DISCREPANT_TESTS = len(tests_with_methods)
    TOTAL_TESTS = len(tests)
    return tests, tests_with_methods


def sum_methods_if_test_exists(traffic_json_path, test_names):
  
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

    for key, _ in traffic_data.items():
        
        val = key.split(".txt")[0]
        # run on cloud if discrepant test
        if val in test_names:
            for request in cost:
                cost[request] += traffic_data[key][request]

    return cost


if __name__ == "__main__":

    methods_json_path = "sdk_methods/Orleans.json"
    methods_file_path = "discrepantApisDotNet.txt"
    traffic_json_path = "application_cost_data/orleans.json"

    total_tests, discrepant_tests = find_tests_with_methods(methods_json_path, methods_file_path)

    print("Test with discrepant methods:")
    for name in discrepant_tests:
        print(name)

    total_cost = sum_methods_if_test_exists(traffic_json_path, total_tests)
    print("*CLOUD COST*")
    for i in total_cost:
        print(i, total_cost[i])
    print()
    total_cost = sum_methods_if_test_exists(traffic_json_path, discrepant_tests)
    print("*CLOUD & EMULATOR COST*")
    for i in total_cost:
        print(i, total_cost[i])
    print()
    print("Total tests: ", TOTAL_TESTS)
    print("Potential discrepant tests: ", DISCREPANT_TESTS)
