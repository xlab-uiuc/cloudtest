import os, subprocess, json
import reference_run
import utils, re


def run_tests(config, tags, rel_path):

    tests = load_test_names(config)   
    results = {}
    env = {"env": "", "test": ""}

    os.system('dotnet build')

    for test in tests:

        print(f'Running test: {test}')
        env["test"] = f'{test}'
        
        if test in tags:
            print(f'Previous run: {tags[test]}')
            env["env"] = tags[test]

            try:
                utils.ping(json.dumps(env), 'empty')
                # run the test
                if 'framework' in config:
                    out = subprocess.check_output(f'dotnet test --no-build --framework {config["framework"]} --filter {test}', shell=True, text=True)
                else:
                    out = subprocess.check_output(f'dotnet test --no-build --filter {test}', shell=True, text=True)
                
                # confirm the test run completion
                try:
                    res = utils.ping("complete_run")
                except:
                    print(f'Ping failed! Error: {e}')
                    results[test] = "PingFailed"
                    continue
                print(f'Ping result: {res}')

                # run reference run if the hashes don't match
                if res == "True":
                    print(f'REFERENCE RUN')
                    results[test], tags[test] = reference_run.run(test, config, rel_path) # ref run if the hashes don't match
                else:
                    pattern = r'(\w+)!\s+-\s+Failed:\s+\d+,\s+Passed:\s+\d+,\s+Skipped:\s+\d+,\s+Total:\s+\d+'
                    match = re.search(pattern, out)
                    if match:
                        results[test] = match.group(1)
                    else:
                        results[test] = "Undefined"
               
            except Exception as e:
                print(f'Error: {e}')
                results[test] = "Failed"

                # doing reference run if the test fails
                print(f'Reference run')
                results[test], tags[test] = reference_run.run(test, config, rel_path)
 
        else:
            print(f'Reference run')
            results[test], tags[test] = reference_run.run(test, config, rel_path)
            
        # save results in detailed logs (need these logs for cost calculation)
        # with open(f'{os.path.join(rel_path,"proxy_logs.txt")}', 'a') as f:
        #     f.write(f'Test Result: {results[test]}\n\n')

    utils.ping("tests_complete", 'empty')

    # need these logs for cost calculation
    # with open(f'{os.path.join(rel_path,"proxy_logs.txt")}', 'a') as f:
    #     f.write(f'Entire run results: {results}\n\n')
        
    return results, tags
    


def load_test_names(config):

    # TO-DO: extend for other test frameworks

    if 'framework' in config:
        print(f"dotnet test --list-tests --framework {config['framework']}")
        out = subprocess.check_output(f"dotnet test --list-tests --framework {config['framework']}", shell=True, text=True)
    else:
        print(f"dotnet test --list-tests")
        out = subprocess.check_output(f"dotnet test --list-tests", shell=True, text=True) 
    start_index = out.find("The following Tests are available:") 
    tests = out[start_index+len("The following Tests are available:"):len(out)-1]
    tests = [test.strip() for test in tests.split("\n") if test.strip()]
    tests = [test.split('(')[0].strip() for test in tests]
    tests = list(set(tests))   # remove duplicates
    print(f"tests: {tests}")

    return tests







def start():

    # TO-DO: Customize test command based on the test framework

    # TO-DO: In Github Actions
    
    # TO-DO: Capture the test names from an external script (should be provided by the developer)

    print("Starting script execution...")

    config = utils.load_config()
    tags = utils.load_tags() 

    # change directory to the test folder and run the tests
    main_path = os.getcwd()
    path = os.path.join(main_path, config['test_path'])
    rel_path = os.path.relpath(main_path, path)
    os.chdir(path)
    print(f'Current directory: {os.getcwd()}')
    results, tags = run_tests(config, tags, rel_path)
    os.chdir(main_path)

    utils.save_results(results) 
    utils.save_tags(tags)

    print("Script execution completed.")





start()
