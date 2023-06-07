from contextlib import redirect_stdout
from containerclient import ContainerClient
from blobclient import BlobClient
from blobserviceclient import MyBlobServiceClient
from tableclient import MyTableClient
from tableserviceclient import MyTableServiceClient
from queueclient import MyQueueClient
from queueserviceclient import MyQueueServiceClient
import io
import itertools


'''
Total operations
Azure Blob (we take 3 clients and ignore lease client): 63
Azure Table: 19
'''

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


def run_ops(arg, methods, test_cloud, test_em, t_count, count, buf, discrepant_methods):

    for method in methods:
            t_count += 1
            if method in discrepant_methods:
                t_count += 1 

            try:
                if not method(test_cloud, arg[t_count]) == method(test_em, arg[t_count]) and not method.__name__ in discrepant_methods:
                    count += 1
                    output = buf.getvalue().strip()

                    # empty buffer
                    buf.truncate(0)

                    discrepant_methods.append(method.__name__)

                    with open('discrepancy.txt', 'a') as f:
                        f.write(method.__name__ + '\n\n' + output)
                        f.write(f'\n\n\n{count}/{t_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
            except Exception as e:
                print("Exception: ", e)

    return discrepant_methods, t_count, count


def run_sequences():
    
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
                if method in methods_blobClient and not method(test_cloud_bc) == method(test_em_bc) or method in methods_containerClient and not method(test_cloud_cc) == method(test_em_cc) or method in methods_blobServiceClient and not method(test_cloud_bsc) == method(test_em_bsc):
                    
                    count += 1
                    output = buf.getvalue().strip()

                    with open('discrepancy.txt', 'a') as f:
                        f.write('\n'.join(i.__name__ for i in list_seqs[counter]) + '\n\n' + output)
                        f.write(f'\n\n\n{count}/{t_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
                    list_seqs = list_seqs[:counter+1] + [list_seqs[i] for i in range(counter, len(list_seqs)) if not check_sublist_in_list(list(list_seqs[i]), sublist)]
                    break

        counter += 1

    extract_discrepancy('discrepancy.txt')


def run1v1(arg):

    # get all methods of all the clients
    methods_blobClient = [getattr(BlobClient, attr) for attr in dir(BlobClient) if callable(getattr(BlobClient, attr)) and not attr.startswith("__")]
    methods_containerClient = [getattr(ContainerClient, attr) for attr in dir(ContainerClient) if callable(getattr(ContainerClient, attr)) and not attr.startswith("__")]
    methods_blobServiceClient = [getattr(MyBlobServiceClient, attr) for attr in dir(MyBlobServiceClient) if callable(getattr(MyBlobServiceClient, attr))
     and not attr.startswith("__")]
    methods_tableClient = [getattr(MyTableClient, attr) for attr in dir(MyTableClient) if callable(getattr(MyTableClient, attr)) and not attr.startswith("__")]
    methods_tableServiceClient = [getattr(MyTableServiceClient, attr) for attr in dir(MyTableServiceClient) if callable(getattr(MyTableServiceClient, attr)) and not attr.startswith("__")]
    methods_queueClient = [getattr(MyQueueClient, attr) for attr in dir(MyQueueClient) if callable(getattr(MyQueueClient, attr)) and not attr.startswith("__")]
    methods_queueServiceClient = [getattr(MyQueueServiceClient, attr) for attr in dir(MyQueueServiceClient) if callable(getattr(MyQueueServiceClient, attr)) and not attr.startswith("__")]
    total_methods = methods_blobClient + methods_containerClient + methods_blobServiceClient + methods_tableClient + methods_tableServiceClient + methods_queueClient + methods_queueServiceClient
    # logging.basicConfig(level=logging.DEBUG)

    if arg == ():
        arg = [()] * len(total_methods)

    f = open("discrepant_methods.txt", "w+")
    discrepant_methods = f.read().split('\n')
    f.close()

    # test_cloud_bc = BlobClient(False)
    # test_em_bc = BlobClient()
    # test_cloud_cc = ContainerClient(False)
    # test_em_cc = ContainerClient()
    # test_cloud_bsc = MyBlobServiceClient(False)
    # test_em_bsc = MyBlobServiceClient()
    # test_cloud_tc = MyTableClient(False)
    # test_em_tc = MyTableClient()
    # test_cloud_tsc = MyTableServiceClient(False)
    # test_em_tsc = MyTableServiceClient()
    test_cloud_qc = MyQueueClient(False)
    test_em_qc = MyQueueClient()
    test_cloud_qsc = MyQueueServiceClient(False)
    test_em_qsc = MyQueueServiceClient()

    count = 0
    t_count = -1
    
    with open('discrepancy.txt', 'w') as f:
        f.write('')


    with io.StringIO() as buf, redirect_stdout(buf):

        # # run blob client ops
        # discrepant_methods, t_count, count = run_ops(arg, methods_blobClient, test_cloud_bc, test_em_bc, t_count, count, buf, discrepant_methods)
        # # run container client ops
        # discrepant_methods, t_count, count = run_ops(arg, methods_containerClient, test_cloud_cc, test_em_cc, t_count, count, buf, discrepant_methods)
        # # run blob service client ops
        # discrepant_methods, t_count, count = run_ops(arg, methods_blobServiceClient, test_cloud_bsc, test_em_bsc, t_count, count, buf, discrepant_methods)
        # # run table client ops
        # discrepant_methods, t_count, count = run_ops(arg, methods_tableClient, test_cloud_tc, test_em_tc, t_count, count, buf, discrepant_methods)
        # # run table service client ops
        # discrepant_methods, t_count, count = run_ops(arg, methods_tableServiceClient, test_cloud_tsc, test_em_tsc, t_count, count, buf, discrepant_methods)
        # run queue client ops
        discrepant_methods, t_count, count = run_ops(arg["0"], methods_queueClient, test_cloud_qc, test_em_qc, t_count, count, buf, discrepant_methods)
        # run queue service client ops
        discrepant_methods, t_count, count = run_ops(arg["1"], methods_queueServiceClient, test_cloud_qsc, test_em_qsc, t_count, count, buf, discrepant_methods)

    with open('discrepancy.txt', 'a') as f:
        f.write(f'{count}/{t_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        f.write('Round ended')

    print(discrepant_methods)
    with open('discrepant_methods.txt', 'w') as f:
        f.write("\n".join(discrepant_methods))         
    print('done')
    extract_discrepancy('discrepancy.txt')
    print('done')


'''test suites'''
def main(arg):
    # methods_tableClient = [getattr(MyTableClient, attr) for attr in dir(MyTableClient) if callable(getattr(MyTableClient, attr)) and not attr.startswith("__")]
    # methods_tableServiceClient = [getattr(MyTableServiceClient, attr) for attr in dir(MyTableServiceClient) if callable(getattr(MyTableServiceClient, attr)) and not attr.startswith("__")]
    # methods = methods_tableClient + methods_tableServiceClient
    # print(len(methods))

    run1v1(arg)
    print('done')
    # run_sequences()


'''Get fuzz data'''
if __name__ == '__main__':
    arg = ()
    main(arg)
    
    


    