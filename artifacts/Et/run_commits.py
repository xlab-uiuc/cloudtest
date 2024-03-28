import subprocess
import os, json, time, argparse


def get_latest_commit_hash(commits_count: int) -> str or None:
    try:
        hash_output = subprocess.check_output(["git", "log", "--format=%H", "-n", str(commits_count)]).decode("utf-8").strip().split("\n")[-1]
        return hash_output
    except subprocess.CalledProcessError as e:
        print(f"Error getting commit hash: {e}")
        return None
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--commits_count", type=int, default=5)
    parser.add_argument("--branch_name", type=str, default="main")
    args = parser.parse_args()

    commits_count = args.commits_count
    branch_name = args.branch_name

    # create proxy_logs.txt
    with open("proxy_logs.txt", 'w') as f:
        f.write('')

    # create hashes.json
    with open("hashes.json", 'w') as f:
        f.write('{}')

    # create tags.json
    with open("tags.json", 'w') as f:
        f.write('{}')

    # create dotnet_logs.txt
    with open("dotnet_logs.txt", 'w') as f:
        f.write('')

    # create responses.txt
    with open("responses.txt", 'w') as f:
        f.write('')


    for i in range(commits_count, 0, -1):

        # with open("proxy_logs.txt", 'a') as f:
        #     f.write(f'Commit number: {i}\n')

        hash = get_latest_commit_hash(i)
        out = subprocess.check_output(["git", "checkout", "-b", f"newbranch_{hash}", hash])
        print(out)
        # start timer
        start = time.time()

        os.system('python3 driver.py')

        # end timer
        end = time.time()
        print(f"Time taken: {end - start}")

        out = subprocess.check_output(["git", "checkout", f'{branch_name}'])
        print(out)
        subprocess.check_output(["git", "branch", "-d", f"newbranch_{hash}"])

        commits_count = commits_count - 1

        # copy hashes.json to a new file
        with open("hashes.json") as f:
            hashes = json.load(f)
            with open(f"hashes_{commits_count}.json", 'w') as f:
                f.write(json.dumps(hashes, indent=4))
