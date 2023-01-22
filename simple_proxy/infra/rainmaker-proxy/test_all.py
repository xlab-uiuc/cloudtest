import os
import argparse
from utils import find_latest_dir

if __name__ == "__main__":
    proj               = "Orleans"
    raw_stat_directory = find_latest_dir(os.path.join(os.getcwd(), "stat"))
    outcome_directory  = find_latest_dir("outcome")
    # raw_stat_directory = "Orleans-emulator_2022.10.14.01.50.11"
    # outcome_directory = "Orleans-emulator_2022.10.14.01.50.11"
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--proj", default = proj, help="Project")
    parser.add_argument("-r", "--raw_stat_directory", default = raw_stat_directory, help="")
    parser.add_argument("-o", "--outcome_directory", default = outcome_directory, help="")
    args = parser.parse_args()

    open('log.txt', 'w').close()
    # -u is for PUT
    os.system("python ./test_raw_data_generator.py -d " + args.raw_stat_directory + "  -u False 1>>log.txt")


    os.system("python ./test_outcome_generator.py -d " + args.outcome_directory + " -p " + args.proj + " 1>>log.txt")

    