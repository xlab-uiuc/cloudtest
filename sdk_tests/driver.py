from contextlib import redirect_stdout
from containerclient import ContainerClient
from blobclient import BlobClient
from blobserviceclient import MyBlobServiceClient
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
    methods_blobClient = [getattr(BlobClient, attr) for attr in dir(BlobClient) if callable(getattr(BlobClient, attr)) and not attr.startswith("__")]
    methods_containerClient = [getattr(ContainerClient, attr) for attr in dir(ContainerClient) if callable(getattr(ContainerClient, attr)) and not attr.startswith("__")]
    methods_blobServiceClient = [getattr(MyBlobServiceClient, attr) for attr in dir(MyBlobServiceClient) if callable(getattr(MyBlobServiceClient, attr)) and not attr.startswith("__")]
    methods = methods_blobClient + methods_containerClient + methods_blobServiceClient
    # logging.basicConfig(level=logging.DEBUG)

    test_cloud_bc = BlobClient(False)
    test_em_bc = BlobClient()
    test_cloud_cc = ContainerClient(False)
    test_em_cc = ContainerClient()
    test_cloud_bsc = MyBlobServiceClient(False)
    test_em_bsc = MyBlobServiceClient()
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
                if method in methods_blobClient and not method(test_cloud_bc) == method(test_cloud_bc) or method in methods_containerClient and not method(test_cloud_cc) == method(test_em_cc) or method in methods_blobServiceClient and not method(test_cloud_bsc) == method(test_em_bsc):
                    
                    count += 1
                    output = buf.getvalue().strip()

                    with open('discrepancy.txt', 'a') as f:
                        f.write('\n'.join(i.__name__ for i in list_seqs[counter]) + '\n\n' + output)
                        f.write(f'\n\n\n{count}/{t_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
                    list_seqs = list_seqs[:counter+1] + [list_seqs[i] for i in range(counter, len(list_seqs)) if not check_sublist_in_list(list(list_seqs[i]), sublist)]
                    break

        counter += 1

    extract_discrepancy('discrepancy.txt')