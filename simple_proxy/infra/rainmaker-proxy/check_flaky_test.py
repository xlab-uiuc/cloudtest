import os
import argparse
import csv

descp = "This is file for prune out flaky tests. Now we compare three results. The final result will store in the project name folder"

def_proj = "orleans"


def_round_1 = "Orleans-realService-no-proxy_2022.10.10.19.12.17"
def_round_2 = "Orleans-realService-no-proxy_2022.10.11.14.44.21"
def_round_3 = "Orleans-realService-no-proxy_2022.10.11.16.50.45"



parser = argparse.ArgumentParser(
    description=descp, formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("--round1", "-r1", default=def_round_1,
                    help="The first round for comparision")
parser.add_argument("--round2", "-r2", default=def_round_2,
                    help="The second round for comparision")
parser.add_argument("--round3", "-r3", default=def_round_3,
                    help="The third round for comparision")
parser.add_argument("--project", "-p", default=def_proj,
                    help="The project name")



args = parser.parse_args()

# result_dir = os.path.join("outcome", args.round)   #outcome/
# stat_dir = os.path.join("stat", args.round)        #stat/
def remove_flaky(output_dir_proj, dir_result1, dir_result2, dir_result3):

    tmp_file = os.path.join(output_dir_proj,"Stable_tests.csv")
    
    pass_1, pass_2, pass_3 = [] , [] ,[]
    pass_all = [pass_1, pass_2, pass_3]
    result_all = [dir_result1, dir_result2, dir_result3]
    for i in range(3):
        
        tmp_result =  os.path.join(result_all[i],"PASSED_test.csv")

        with open(tmp_result, "r", encoding="utf-8" ) as csvfile:
            reader = csv.reader(csvfile)
            pass_all[i] = [row[0] for row in reader]
            # print(pass_all[i])
    pass_1 = pass_all[0]
    pass_2 = pass_all[1]
    pass_3 = pass_all[2]
    intersection = list( set(pass_1).intersection(pass_2, pass_3) ) 

    f = open(tmp_file, "w", encoding="utf-8")
    for i in intersection:
        f.write(i + "\n")
    f.close()

    return


if __name__ == "__main__":
    
    output_dir_proj = os.path.join("../../results", args.project)
    output_dir_round1 = os.path.join("../../results", args.round1)
    output_dir_round2 = os.path.join("../../results", args.round2)
    output_dir_round3 = os.path.join("../../results", args.round3)
    remove_flaky(output_dir_proj, output_dir_round1, output_dir_round2, output_dir_round3)