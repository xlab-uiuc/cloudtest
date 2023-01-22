from msilib.schema import Directory
import pandas as pd
import xml.etree.ElementTree as ET
import os
import shutil
import argparse
import pathlib
from utils import find_latest_dir, create_test_run_result_dir

class OutcomeGenerator:
    num_of_file = 0
    num_of_test = 0

    pass_cnt = 0
    fail_cnt = 0
    skip_cnt = 0
    total_test_runs = 0

    pass_result_set = set()
    failed_result_set = set()
    skipped_result_set = set()
    all_tests_names_set = set()
    all_tests_names_list = []
    tests_result_dict = {}

    def __init__(self, _result_dir_str, _proj_name, _new_run_dir):
        self.result_dir_str = _result_dir_str
        self.directory = os.fsencode(_result_dir_str)
        self.proj_name = _proj_name
        self.new_run_dir = _new_run_dir

    def generate(self):
        for file in os.listdir(self.directory):
            test_dir_name = os.fsdecode(file)
            dir_str = self.result_dir_str + "/" + test_dir_name
            # print(dir_str)
            if os.path.isdir(dir_str):
                self.num_of_test += 1
                for path in os.listdir(dir_str):
                    num_file = []
                    result_file_path = os.path.join(dir_str, path)
                    if os.path.isfile(result_file_path):
                        self.num_of_file += 1
                        num_file.append(result_file_path)
                        # print(result_file_path)
                        tree = ET.parse(result_file_path)
                        root = tree.getroot()

                        if root.find('.//{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}Results') == None:
                            # If a test was blamed during running, it will not have Results leaf in XML
                            print("Blamed tests: {}".format(test_dir_name))
                            # So we need to use ResultSummary instead
                            child = root.find(
                                './/{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}ResultSummary')
                            self.all_tests_names_set.add(test_dir_name)
                            self.all_tests_names_list.append(test_dir_name)
                            if child.attrib.get('outcome') == "Passed":
                                self.pass_cnt += 1
                                self.pass_result_set.add(test_dir_name)
                                self.tests_result_dict[test_dir_name] = "Passed"
                            elif child.attrib.get('outcome') == "Failed":
                                self.fail_cnt += 1
                                self.failed_result_set.add(test_dir_name)
                                self.tests_result_dict[test_dir_name] = "Failed"
                            elif child.attrib.get('outcome') == "NotExecuted":
                                self.skip_cnt += 1
                                self.skipped_result_set.add(test_dir_name)
                                self.tests_result_dict[test_dir_name] = "Skipped"
                        else:
                            children = root.find('.//{http://microsoft.com/schemas/VisualStudio/TeamTest/2010}Results')
                            for child in children:
                                # print(child.attrib.get('outcome'))
                                self.all_tests_names_set.add(test_dir_name)
                                self.all_tests_names_list.append(test_dir_name)
                                if child.attrib.get('outcome') == "Passed":
                                    self.pass_cnt += 1
                                    self.pass_result_set.add(test_dir_name)
                                    self.tests_result_dict[test_dir_name] = "Passed"
                                elif child.attrib.get('outcome') == "Failed":
                                    self.fail_cnt += 1
                                    self.failed_result_set.add(test_dir_name)
                                    self.tests_result_dict[test_dir_name] = "Failed"
                                elif child.attrib.get('outcome') == "NotExecuted":
                                    self.skip_cnt += 1
                                    self.skipped_result_set.add(test_dir_name)
                                    self.tests_result_dict[test_dir_name] = "Skipped"
                    if len(num_file) > 1:
                        print("Num of file under {} is larger than 1".format(dir_str))
        self.__print_output_stat()
        self.__write_output()
        self.__copy_f_to_result_dir()

    def __print_output_stat(self):
        self.total_test_runs = self.pass_cnt + self.fail_cnt + self.skip_cnt
        print("TOTAL # unit tests to run: {}".format(self.num_of_test))
        print("TOTAL # test rounds to run: {}".format(self.total_test_runs))
        print("# of files: {}".format(self.num_of_file))
        print("# PASSED tests: {}".format(self.pass_cnt))
        print("# FAILED tests: {}".format(self.fail_cnt))
        print("# SKIPPED tests: {}".format(self.skip_cnt))
    
    # Write outcome results to files.
    def __write_output(self):
        # Stat file output
        stat_file = open(self.new_run_dir + "/test-stats.txt", "w+")
        stat_file.write("TOTAL # unit tests to run: {}\n".format(self.num_of_test))
        stat_file.write("TOTAL # test rounds to run: {}\n".format(self.total_test_runs))
        stat_file.write("# PASSED tests: {}\n".format(self.pass_cnt))
        stat_file.write("# FAILED tests: {}\n".format(self.fail_cnt))
        stat_file.write("# SKIPPED tests: {}\n".format(self.skip_cnt))
        stat_file.close()

        # PASSED test output
        pass_file = open(self.new_run_dir + "/PASSED_test.csv", "w+")
        for ele in sorted(self.pass_result_set):
            pass_file.write("{}\n".format(ele))
        pass_file.close()

        # FAILED test output
        fail_file = open(self.new_run_dir + "/FAILED_test.csv", "w+")
        for ele in sorted(self.failed_result_set):
            fail_file.write("{}\n".format(ele))
        fail_file.close()

        # SKIPPED test output
        skip_file = open(self.new_run_dir + "/SKIPPED_test.csv", "w+")
        for ele in sorted(self.skipped_result_set):
            skip_file.write("{}\n".format(ele))
        skip_file.close()
    
    # Copy the files to the destination result dir (name in lower case)
    def __copy_f_to_result_dir(self):
        for f in os.listdir(self.new_run_dir):
            src_file_path = os.path.join(self.new_run_dir, f)
            print(os.path.join(self.new_run_dir, f))
            dst_dir_path = os.path.join(self.new_run_dir, "..", self.proj_name)
            dst_file_path = os.path.join(self.new_run_dir, "..", self.proj_name, f)
            if_dir_exist = os.path.isdir(dst_dir_path)
            print(dst_dir_path, if_dir_exist)
            if not if_dir_exist:
                os.makedirs(dst_dir_path)
            shutil.copyfile(src_file_path, dst_file_path)
    

if __name__ == "__main__":
    def_proj = "orleans"
    def_directory = find_latest_dir("outcome")
    # def_directory = "outcome/Akka.Persistence.Azure-injection-round-status-code_2022.06.03.14.46.12"
    # print(def_directory)
    # Latest outcomes:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir", default = def_directory, help="The directory to run analysis")
    parser.add_argument("-p", "--proj", default = def_proj, help="The project to persist the results for")
    args = parser.parse_args()
    if args.dir != def_directory:
        tar_dir = "outcome/" + args.dir
    else:
        tar_dir = args.dir

    # print(tar_dir)
    # latest_outcome_dir = find_latest_dir("outcome")
    latest_outcome_dir = tar_dir
    # dir_name = return_latest_dir_name("outcome")
    dir_name = pathlib.PurePath(tar_dir).name
    latest_result_dir = create_test_run_result_dir(os.path.join("..", "..", "results"), dir_name)
    og = OutcomeGenerator(latest_outcome_dir, args.proj, latest_result_dir)
    og.generate()



