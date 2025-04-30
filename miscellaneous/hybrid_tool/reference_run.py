import os, json, subprocess
import utils, re


def run_test(test_name, config, rel_path):

    
    try:
        if 'framework' in config:
            out = subprocess.check_output(f'dotnet test --no-build --framework {config["framework"]} --filter {test_name}', shell=True, text=True)
        else:
            out = subprocess.check_output(f'dotnet test --no-build --filter {test_name}', shell=True, text=True)

        try:
            utils.ping("complete_reference_run")
        except Exception as e:
            print(f'Ping failed! Error: {e}')
            return "PingFailed"

        pattern = r'(\w+)!\s+-\s+Failed:\s+\d+,\s+Passed:\s+\d+,\s+Skipped:\s+\d+,\s+Total:\s+\d+'
        match = re.search(pattern, out)
        if match:
            res = match.group(1)
        else:
            res = "Undefined"
        return res
    
    except:
        return "Failed"



def run(test_name, config, rel_path):


    # load env
    env = {"env": "", "test": f"{test_name}"}

    print(f'Test: {test_name}')

    # emulator run
    env["env"] = "emulator"
    utils.ping(json.dumps(env), 'empty')
    result_emulator = run_test(test_name, config, rel_path)
    print(f'Emulator result: {result_emulator}')

    # save results in detailed logs
    # with open(f'{os.path.join(rel_path,"proxy_logs.txt")}', 'a') as f:
    #     f.write(f'Test Result: {result_emulator}\n\n')

    # cloud run
    if not result_emulator == "Skipped":
        env["env"] = "cloud"
        utils.ping(json.dumps(env), 'empty')
        result_cloud = run_test(test_name, config, rel_path)
        print(f'Cloud result: {result_cloud}')
    else:
        result_cloud = "Skipped"

    # compare results and update tags
    tag = ''
    if result_cloud == result_emulator:
        tag = "emulator"
    else:
        tag = "cloud"
    
    return result_cloud, tag

