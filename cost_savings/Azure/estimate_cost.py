import json

from matplotlib import pyplot as plt
import numpy as np

TOTAL_TESTS = 0
DISCREPANT_TESTS = 0
DISCREPANT_METHODS = []
METHODS_COUNT = {}
TEST_METHOD_MAP = {}

def get_methods_from_file(file_path):
    
    with open(file_path, "r") as f:
        methods = f.read().splitlines()

    return methods



def find_tests_with_methods(methods_json_path, methods):
    global DISCREPANT_TESTS
    global TOTAL_TESTS
    global METHODS_COUNT
    global TEST_METHOD_MAP
    global DISCREPANT_METHODS
    
    with open(methods_json_path, "r") as f:
        json_data = json.load(f)

    tests = json_data.keys()

    app_tests = 0
    for i in tests:
        if not json_data[i] == []: # remove tests with no cloud methods
            app_tests += 1

    tests_with_methods = []
    test_methods_count = {}
    discrepant_methods = []
    for key, value in json_data.items():
        for i in value:
            if i in test_methods_count:
                test_methods_count[i] += 1
            else:
                test_methods_count[i] = 1
        for method in methods:
            if method in value:
                # print(method)
                if not method in discrepant_methods:
                    discrepant_methods.append(method)
                if not key in tests_with_methods:
                    tests_with_methods.append(key)

                if not method in DISCREPANT_METHODS:
                    DISCREPANT_METHODS.append(method)
                
                if not key in TEST_METHOD_MAP:
                    TEST_METHOD_MAP[key] = [method]
                else:
                    TEST_METHOD_MAP[key].append(method)
                # no need to check for other discrepant methods in this test hence break
                # break

    for i in test_methods_count:
        if i in METHODS_COUNT:
            METHODS_COUNT[i] += test_methods_count[i]
        else:
            METHODS_COUNT[i] = test_methods_count[i]

    print(f'Method counts: {json.dumps(test_methods_count, indent=2)}')
    print(f'Unique API methods: {len(test_methods_count)}')
    print(f'Discrepant Unique APIs: {len(discrepant_methods)}')
    print(f'Discrepant APIs: \n{[(i,test_methods_count[i]) for i in discrepant_methods]}')
    print(f'Potential discrepant tests: {len(tests_with_methods)}')
    print(f'Total tests: {app_tests}\n\n')

    DISCREPANT_TESTS += len(tests_with_methods)
    TOTAL_TESTS += app_tests

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


# create an api popularity graph against discrepancies
def create_graph(x, y_line, y_bar, x_label, y_label, title):
    fig, ax_line = plt.subplots(1, 1)
    ax_line.plot(x, y_line, 'r')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    ax_line.set_zorder(1)
    ax_line.patch.set_visible(False)
    ax_bar = plt.twinx()
    ax_bar.bar(x, y_bar)
    fig.set_zorder(ax_bar.get_zorder() + 1)
    plt.ylabel("Discrepant APIs Popularity")
    plt.title(title)
    plt.savefig("cost_saving.png")
    plt.show()

    
def run_all_apps():

    global DISCREPANT_TESTS
    global TOTAL_TESTS

    apps = ['alpakka','orleans','identityazuretable','ironpigeon','sleet','attachmentplugin','snowmaker', 'insights', 'durabletask', 'streamstone']
    # apps = ['streamstone']
    methods_file_path = "discrepantApisEmulator.txt"
    methods = get_methods_from_file(methods_file_path)
    
    for j in apps:

        methods_json_path = f"application_sdk_methods/{j}.json"
        traffic_json_path = f"application_request_types/{j}.json"

        print(f'\nApp: {j} ----- Started\n\n')
        total_tests, discrepant_tests = find_tests_with_methods(methods_json_path, methods)

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
        print('\n----------------------------------------------\n')

    print("Total tests: ", TOTAL_TESTS)
    print("Potential discrepant tests: ", DISCREPANT_TESTS)


if __name__ == "__main__":

    run_all_apps()

    

    
    
        


# paste it in main to get the graph

# sort methods by count
METHODS_COUNT = {k: v for k, v in sorted(METHODS_COUNT.items(), key=lambda item: item[1], reverse=True)}

# print(json.dumps(METHODS_COUNT, indent=2))
arr = np.array(list(METHODS_COUNT.values()))

# x-axis: weighted popularity of methods
# ratio = arr/arr.sum() * 100
# cumulative_x = np.cumsum(ratio)
# x_axis = cumulative_x


# x-axis: all methods used in the tests
x_axis = np.arange(1, len(METHODS_COUNT)+1)


# x-axis: only discrepant methods
# x_axis = np.arange(0, len(DISCREPANT_METHODS)+1)

y_axis = []
# y_axis.append(len([j for j in TEST_METHOD_MAP.keys() if not TEST_METHOD_MAP[j] == []]))
for i in METHODS_COUNT.keys():
    if i in DISCREPANT_METHODS:
        for j in TEST_METHOD_MAP.keys():
            if i in TEST_METHOD_MAP[j]:
                TEST_METHOD_MAP[j].pop(TEST_METHOD_MAP[j].index(i))

    y_axis.append(len([j for j in TEST_METHOD_MAP.keys() if not TEST_METHOD_MAP[j] == []]))

y_axis = np.array(y_axis)
# scale between 0 and 100
y_axis = ((y_axis - y_axis.min())/(y_axis.max() - y_axis.min())) * 1.0
create_graph(x_axis, y_axis, arr, "Fixed Discrepant APIs (Descending Order of Popularity)", "Test Discrepancies", "")


