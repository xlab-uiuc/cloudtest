import os, subprocess, json, platform, argparse
AZURE_NAME_SPACE = ["Azure.Storage.Blobs", "Azure.Storage.Queues", "Azure.Data.Tables"]

def getTestList():
    tests = {}
    with open("./tests.txt") as f:
        for line in f.readlines():
            tests[str(line).strip()] = set()
    return tests

def parse_log_segment(segment, tests, test):
    lines = segment.split("\n")
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        for namespace in AZURE_NAME_SPACE:
            if namespace in line:
                method_name = line.split(".")[-1]
                method_name = method_name[0 : method_name.find("(")]
                tests[test].add(method_name)
                return

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def compile_json(tests: dict):
    with open("output.json", "w") as jsonFile:
        json.dump(tests, jsonFile, ensure_ascii=False, indent=4, default=set_default)

def run_tests():
    tests = getTestList()
    log_folder = os.path.join(os.getcwd(), 'logs')
    os.makedirs(log_folder, exist_ok=True)
    
    for test in tests.keys():
        file_name = test.replace(":", "_").replace("\"", "") + ".txt"
        print(f"Processing test: {test}")
        abusolute_path = os.path.join(log_folder, file_name)
        if (platform.system() == 'Windows'):
            abusolute_path = u"\\\\?\\" + abusolute_path
        with open(abusolute_path, 'wb') as f:    
            test_cmd = f"dotnet test --filter \"{test}\""
            print(f"cmd: {test_cmd}")
            p = subprocess.Popen(test_cmd, stdout=subprocess.PIPE, shell=True)
            f.write(p.stdout.read())
        # Parse the results
        with open(abusolute_path, 'r') as f:
            full_log = f.read()
            segments = full_log.split("---Cloudtest---")
            for segment in segments:
                parse_log_segment(segment, tests, test)
                
        print(f"Find the following method: {str(tests[test])}")

    compile_json(tests)

def compile_json_without_run_test():
    tests = getTestList()
    log_folder = os.path.join(os.getcwd(), 'logs')
    for test in tests.keys():
        file_name = test.replace(":", "_").replace("\"", "") + ".txt"
        print(f"Processing test: {test}")
        abusolute_path = os.path.join(log_folder, file_name)
        if (platform.system() == 'Windows'):
            abusolute_path = u"\\\\?\\" + abusolute_path

        with open(abusolute_path, 'r') as f:
            full_log = f.read()
            segments = full_log.split("---Cloudtest---")
            for segment in segments:
                parse_log_segment(segment, tests, test)
                
        print(f"Find the following method: {str(tests[test])}")

    compile_json(tests)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument('--compile', action='store_true', help='with this flag script will only parse json from the log without running the test')
    args = parser.parse_args()
    if (args.compile):
        compile_json_without_run_test()
    else:
        run_tests()