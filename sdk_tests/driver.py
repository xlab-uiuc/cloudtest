from contextlib import redirect_stdout
from containerclient import ContainerClient
from blobclient import BlobClient
import io
import itertools




'''Check if a sublist exists in a list'''
def check_sublist_in_list(given_list, sublist):
    res = False
    for idx in range(len(given_list) - len(sublist) + 1):
        if given_list[idx: idx + len(sublist)] == sublist:
            res = True
            break

    return res


'''Get last log aka discrepant'''
def get_last_log(li):
    # reverse loop
    for i in range(len(li)-1, -1, -1):
        if '**AZURE**' in li[i]:
            return li[i] + '\n' + li[i+1]



'''Extract discrepancys from the output of the test'''
def extract_discrepancy(file):
    # load content of file
    li = []
    with open(file, 'r') as f:
        content = f.read()
        content = content.split('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        for i in content:
            log = get_last_log(i.split('\n'))
            if log and log not in li:
                li.append(log)

    # write to file
    with open('unique_discrepancy.txt', 'w') as f:
        f.write('\n\n'.join(li))




'''Get all the test functions'''
if __name__ == '__main__':



    # get all methods of ContainerClient
    methods = [getattr(BlobClient, attr) for attr in dir(BlobClient) if callable(getattr(BlobClient, attr)) and not attr.startswith("__")]

    # logging.basicConfig(level=logging.DEBUG)

    test_cloud = BlobClient(False)
    test_em = BlobClient()
    count = 0
    t_count = 0
    list_seqs = list(itertools.combinations(methods, 5))

    with open('discrepancy.txt', 'w') as f:
        f.write('')

    counter = 0
    while counter < len(list_seqs):
        t_count += 1
        
        with io.StringIO() as buf, redirect_stdout(buf):
            sublist = []

            for method in list_seqs[counter]:
                sublist.append(method)
                if not method(test_cloud) == method(test_em):
                    
                    count += 1
                    output = buf.getvalue().strip()

                    with open('discrepancy.txt', 'a') as f:
                        f.write('\n'.join(i.__name__ for i in list_seqs[counter]) + '\n\n' + output)
                        f.write(f'\n\n\n{count}/{t_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
                    list_seqs = list_seqs[:counter+1] + [list_seqs[i] for i in range(counter, len(list_seqs)) if not check_sublist_in_list(list(list_seqs[i]), sublist)]
                    break

        counter += 1

    extract_discrepancy('discrepancy.txt')