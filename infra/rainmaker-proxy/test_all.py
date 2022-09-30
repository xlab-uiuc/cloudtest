import os
from utils import return_latest_dir_name, find_latest_dir

#if not default, add stat/before the name

# TODO: make all these configurable 
# Based on the config.json file => automatically set these up

# For DistributedLock
proj = "distributedlock"
raw_stat_directory = "DistributedLock_2022.05.13.05.29.54"
stat_directory = "DistributedLock_2022.05.13.05.29.54"
outcome_directory = "DistributedLock_2022.05.13.05.29.54"

# raw_stat_directory = find_latest_dir(os.path.join(os.getcwd(), "stat"))
# stat_directory = find_latest_dir("stat")
# outcome_directory = find_latest_dir("outcome")

if __name__ == "__main__":
    open('log.txt', 'w').close()
    # -u is for PUT
    os.system("python ./test_raw_data_generator.py -d " + raw_stat_directory + "  -u False 1>>log.txt")
    # os.system("python ./test_raw_data_generator.py  1>>log.txt")

    os.system("python ./test_stat_generator.py -d " + stat_directory + " -p " + proj + " -u False 1>>log.txt")
    # os.system("python ./test_stat_generator.py 1>>log.txt")

    os.system("python ./test_outcome_generator.py -d " + outcome_directory + " -p " + proj + " 1>>log.txt")
    # os.system("python ./test_outcome_generator.py 1>>log.txt")
    
    
    