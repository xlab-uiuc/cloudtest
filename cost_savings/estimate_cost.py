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

    methods_json_path = "sdk_methods/Alpakka.json"
    methods_file_path = "discrepantApisDotNet.txt"
    traffic_json_path = "application_cost_data/alpakka.json"

    total_tests, discrepant_tests = find_tests_with_methods(methods_json_path, methods_file_path)

    # all tests on the cloud
    cloud_cost = sum_methods_if_test_exists(traffic_json_path, total_tests)
    total = 0
    print("*CLOUD COST*")
    for i in cloud_cost:
        print(i, cloud_cost[i])
        total += cloud_cost[i]
    print("Total: ", total)
    print()

    # a combination of cloud and emulator
    total = 0
    cloud_em_cost = sum_methods_if_test_exists(traffic_json_path, discrepant_tests)
    print("*CLOUD & EMULATOR COST*")
    for i in cloud_em_cost:
        print(i, cloud_em_cost[i])
        total += cloud_em_cost[i]
    print("Total: ", total)
    print()

    total = 0
    print("*SAVINGS*")
    for i in range(len(cloud_cost)):
        saving = cloud_cost[list(cloud_cost.keys())[i]] - cloud_em_cost[list(cloud_em_cost.keys())[i]]
        print(list(cloud_cost.keys())[i], saving)
        total += saving
    print("Total: ", total)
    print()

    print("Total tests: ", TOTAL_TESTS)
    print("Potential discrepant tests: ", DISCREPANT_TESTS)
