import subprocess
import os, json

def get_latest_commit_hash(commits_count: int) -> str or None:
    try:
        hash_output = subprocess.check_output(["git", "log", "--format=%H", "-n", str(commits_count)]).decode("utf-8").strip().split("\n")[-1]
        return hash_output
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit hash: {e}")
        return None
    

if __name__ == "__main__":

    commits_count = 1

    # create proxy_logs.txt
    with open("proxy_logs.txt", 'w') as f:
        f.write('')

    # create hashes.json
    with open("hashes.json", 'w') as f:
        f.write('{}')

    # create tags.json
    with open("tags.json", 'w') as f:
        f.write('{}')

    # create cur_hashes.json
    with open("cur_hashes.json", 'w') as f:
        f.write('{}')

    # create .test_env
    with open(".test_env", 'w') as f:
        f.write('{"env": "", "test": ""}')

    # create dotnet_logs.txt
    with open("dotnet_logs.txt", 'w') as f:
        f.write('')

    # create responses.txt
    with open("responses.txt", 'w') as f:
        f.write('')


    for i in range(commits_count, 0, -1):

        with open("proxy_logs.txt", 'a') as f:
            f.write(f'Commit number: {i}\n')

        hash = get_latest_commit_hash(i)
        out = subprocess.check_output(["git", "checkout", "-b", hash])
        print(out)
        os.system('python3 driver.py')

        out = subprocess.check_output(["git", "checkout", "mymain"])
        print(out)
        subprocess.check_output(["git", "branch", "-d", hash])

        commits_count = commits_count - 1

        # copy hashes.json to a new file
        with open("hashes.json") as f:
            hashes = json.load(f)
            with open(f"hashes_{commits_count}.json", 'w') as f:
                f.write(json.dumps(hashes, indent=4))

        # break