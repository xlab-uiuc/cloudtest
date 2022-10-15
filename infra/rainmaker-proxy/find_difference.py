import os
import argparse
import csv

descp = "This is file for prune out flaky tests. Now we compare three results. The final result will store in the project name folder"

def_proj = "orleans"

parser = argparse.ArgumentParser(
    description=descp, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--project", "-p", default=def_proj,
                    help="The project name")
args = parser.parse_args()


def remove_flaky(output_dir_proj, dir_result1, dir_result2):

    pass1_file = os.path.join(output_dir_proj, dir_result1[:-4]) + "-pass.csv"
    pass2_file = os.path.join(output_dir_proj,dir_result2[:-4]) + "-pass.csv"
    
    pass_1, pass_2 = [] , []
    pass_all = [pass_1, pass_2]
    result_all = [dir_result1, dir_result2]
    for i in range(2):
        
        tmp_result =  os.path.join(output_dir_proj, result_all[i])

        with open(tmp_result, "r", encoding="utf-8" ) as csvfile:
            reader = csv.reader(csvfile)
            pass_all[i] = [row[0] for row in reader]
            # print(pass_all[i])
    pass_1 = pass_all[0]
    pass_2 = pass_all[1]

    pass_in_both = list( set(pass_1).intersection(pass_2) ) 
    pass_in_first = list (set(pass_1).difference(pass_in_both))
    pass_in_second = list (set(pass_2).difference(pass_in_both))
    
    f = open(pass1_file, "w", encoding="utf-8")
    for i in pass_in_first:
        f.write(i + "\n")
    f.close()

    f = open(pass2_file, "w", encoding="utf-8")
    for i in pass_in_second:
        f.write(i + "\n")
    f.close()

    return


if __name__ == "__main__":
    
    output_dir_proj = os.path.join("../../results", args.project)
    base = "Real-NP-Stable_tests.csv"
    cmp = "Emulator-Stable_tests.csv"
    remove_flaky(output_dir_proj, cmp, base)