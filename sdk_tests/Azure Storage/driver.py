from contextlib import redirect_stdout
from containerclient import ContainerClient
from blobclient import BlobClient
from blobserviceclient import MyBlobServiceClient
from tableclient import MyTableClient
from tableserviceclient import MyTableServiceClient
from queueclient import MyQueueClient
from queueserviceclient import MyQueueServiceClient
import io, random
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
    with open('../sdk_tests/Azure Storage/unique_discrepancy.txt', 'a') as f:
        f.write('\n\n'.join(li))


def simple_test_run(flag):
    test_bc = BlobClient(flag)
    # test_cc = ContainerClient(flag)
    # test_bsc = MyBlobServiceClient(flag)
    # test_tc = MyTableClient(flag)
    # test_tsc = MyTableServiceClient(flag)
    # test_qc = MyQueueClient(flag)
    # test_qsc = MyQueueServiceClient(flag)

    # get methods
    methods_bc = [getattr(BlobClient, attr) for attr in dir(BlobClient) if callable(getattr(BlobClient, attr)) and not attr.startswith("__")]
    # methods_cc = [getattr(ContainerClient, attr) for attr in dir(ContainerClient) if callable(getattr(ContainerClient, attr)) and not attr.startswith("__")]
    # methods_bsc = [getattr(MyBlobServiceClient, attr) for attr in dir(MyBlobServiceClient) if callable(getattr(MyBlobServiceClient, attr)) and not attr.startswith("__")]
    # methods_tc = [getattr(MyTableClient, attr) for attr in dir(MyTableClient) if callable(getattr(MyTableClient, attr)) and not attr.startswith("__")]
    # methods_tsc = [getattr(MyTableServiceClient, attr) for attr in dir(MyTableServiceClient) if callable(getattr(MyTableServiceClient, attr)) and not attr.startswith("__")]
    # methods_qc = [getattr(MyQueueClient, attr) for attr in dir(MyQueueClient) if callable(getattr(MyQueueClient, attr)) and not attr.startswith("__")]
    # methods_qsc = [getattr(MyQueueServiceClient, attr) for attr in dir(MyQueueServiceClient) if callable(getattr(MyQueueServiceClient, attr)) and not attr.startswith("__")]
    
    # run methods
    for i in methods_bc:
        i(test_bc)
    # for i in methods_cc:
    #     i(test_cc)
    # for i in methods_bsc:
    #     i(test_bsc)
    # for i in methods_tc:
    #     i(test_tc)
    # for i in methods_tsc:
    #     i(test_tsc)
    # for i in methods_qc:
    #     i(test_qc)
    # for i in methods_qsc:
    #     i(test_qsc)


def run_ops(arg, methods, client, count, buf, discrepant_methods):
    

    t_count = -1
    for method in methods:
            t_count += 1
            
            # if method.__name__ in discrepant_methods:
            #     continue

            # we make a new client in order to run an operation independently
            if client == "bc":
                test_cloud = BlobClient(False)
                test_em = BlobClient()
            elif client == "cc":
                test_cloud = ContainerClient(False)
                test_em = ContainerClient()
            elif client == "bsc":
                test_cloud = MyBlobServiceClient(False)
                test_em = MyBlobServiceClient()
            elif client == "tc":
                test_cloud = MyTableClient(False)
                test_em = MyTableClient()
            elif client == "tsc":
                test_cloud = MyTableServiceClient(False)
                test_em = MyTableServiceClient()
            elif client == "qc":
                test_cloud = MyQueueClient(False)
                test_em = MyQueueClient()
            elif client == "qsc":
                test_cloud = MyQueueServiceClient(False)
                test_em = MyQueueServiceClient()

            try:
                if not method(test_cloud, arg[t_count]) == method(test_em, arg[t_count]):
                    count += 1
                    output = buf.getvalue().strip()

                    if method.__name__ not in discrepant_methods:
                        discrepant_methods.append(method.__name__)

                    with open('../sdk_tests/Azure Storage/discrepancy.txt', 'a') as f:
                        f.write(method.__name__ + '\n\n' + output)
                        f.write(f'\n\n\ncount: {count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
            
            except Exception as e:
                print("Exception: ", e)

    return count


# to-do: implement type

def run_sequences_permuation(arg, type):
    
    # get all methods of all the clients
    methods_blobClient = [getattr(BlobClient, attr) for attr in dir(BlobClient) if callable(getattr(BlobClient, attr)) and not attr.startswith("__")]
    methods_containerClient = [getattr(ContainerClient, attr) for attr in dir(ContainerClient) if callable(getattr(ContainerClient, attr)) and not attr.startswith("__")]
    methods_blobServiceClient = [getattr(MyBlobServiceClient, attr) for attr in dir(MyBlobServiceClient) if callable(getattr(MyBlobServiceClient, attr))
     and not attr.startswith("__")]
    methods_tableClient = [getattr(MyTableClient, attr) for attr in dir(MyTableClient) if callable(getattr(MyTableClient, attr)) and not attr.startswith("__")]
    methods_tableServiceClient = [getattr(MyTableServiceClient, attr) for attr in dir(MyTableServiceClient) if callable(getattr(MyTableServiceClient, attr)) and not attr.startswith("__")]
    methods_queueClient = [getattr(MyQueueClient, attr) for attr in dir(MyQueueClient) if callable(getattr(MyQueueClient, attr)) and not attr.startswith("__")]
    methods_queueServiceClient = [getattr(MyQueueServiceClient, attr) for attr in dir(MyQueueServiceClient) if callable(getattr(MyQueueServiceClient, attr)) and not attr.startswith("__")]
    methods = methods_blobClient + methods_containerClient + methods_blobServiceClient + methods_tableClient + methods_tableServiceClient + methods_queueClient + methods_queueServiceClient

    test_cloud_bc = BlobClient(False)
    test_em_bc = BlobClient()
    test_cloud_cc = ContainerClient(False)
    test_em_cc = ContainerClient()
    test_cloud_bsc = MyBlobServiceClient(False)
    test_em_bsc = MyBlobServiceClient()
    test_cloud_tc = MyTableClient(False)
    test_em_tc = MyTableClient()
    test_cloud_tsc = MyTableServiceClient(False)
    test_em_tsc = MyTableServiceClient()
    test_cloud_qc = MyQueueClient(False)
    test_em_qc = MyQueueClient()
    test_cloud_qsc = MyQueueServiceClient(False)
    test_em_qsc = MyQueueServiceClient()

    count = 0
    t_count = 0
    list_seqs = list(itertools.combinations(methods, 5))

    counter = 0
    while counter < len(list_seqs):
        t_count += 1
        
        with io.StringIO() as buf, redirect_stdout(buf):
            sublist = []

            for method in list_seqs[counter]:
                sublist.append(method)
                if method in methods_blobClient and not method(test_cloud_bc) == method(test_em_bc) or method in methods_containerClient and not method(test_cloud_cc) == method(test_em_cc) or method in methods_blobServiceClient and not method(test_cloud_bsc) == method(test_em_bsc) or method in methods_tableClient and not method(test_cloud_tc) == method(test_em_tc) or method in methods_tableServiceClient and not method(test_cloud_tsc) == method(test_em_tsc) or method in methods_queueClient and not method(test_cloud_qc) == method(test_em_qc) or method in methods_queueServiceClient and not method(test_cloud_qsc) == method(test_em_qsc):
                    
                    count += 1
                    output = buf.getvalue().strip()

                    with open('../sdk_tests/Azure Storage/discrepancy.txt', 'a') as f:
                        f.write('\n'.join(i.__name__ for i in list_seqs[counter]) + '\n\n' + output)
                        f.write(f'\n\n\ncount: {count})   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
                    list_seqs = list_seqs[:counter+1] + [list_seqs[i] for i in range(counter, len(list_seqs)) if not check_sublist_in_list(list(list_seqs[i]), sublist)]
                    break

        counter += 1

    extract_discrepancy('discrepancy.txt')



def run1v1(arg):

    # to-do: ordering of methods --> done

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
    t_count = len(total_methods)
    # logging.basicConfig(level=logging.DEBUG)

    # randomize seed
    seed = random.randint(0, 1000000)

    # shuffle all methods
    random.Random(seed).shuffle(methods_blobClient)
    random.Random(seed).shuffle(methods_containerClient)
    random.Random(seed).shuffle(methods_blobServiceClient)
    random.Random(seed).shuffle(methods_tableClient)
    random.Random(seed).shuffle(methods_tableServiceClient)
    random.Random(seed).shuffle(methods_queueClient)
    random.Random(seed).shuffle(methods_queueServiceClient)


    # empty args for default run of ops
    if arg == ():
        arg = {}
        arg['1'] = [[]] * len(methods_blobClient)
        arg['2'] = [[]] * len(methods_containerClient)
        arg['3'] = [[]] * len(methods_blobServiceClient)
        arg['4'] = [[]] * len(methods_tableClient)
        arg['5'] = [[]] * len(methods_tableServiceClient)
        arg['6'] = [[]] * len(methods_queueClient)
        arg['7'] = [[]] * len(methods_queueServiceClient)
    else:
        assert len(arg) == 7, "Invalid number of clients"
        assert len(arg['1']) == len(methods_blobClient), "Invalid number of methods for BlobClient"
        assert len(arg['2']) == len(methods_containerClient), "Invalid number of methods for ContainerClient"
        assert len(arg['3']) == len(methods_blobServiceClient), "Invalid number of methods for BlobServiceClient"
        assert len(arg['4']) == len(methods_tableClient), "Invalid number of methods for TableClient"
        assert len(arg['5']) == len(methods_tableServiceClient), "Invalid number of methods for TableServiceClient"
        assert len(arg['6']) == len(methods_queueClient), "Invalid number of methods for QueueClient"
        assert len(arg['7']) == len(methods_queueServiceClient), "Invalid number of methods for QueueServiceClient"

        for i in arg.items():
            random.Random(seed).shuffle(i[1])


    # do not run discrepant methods again
    f = open("../sdk_tests/Azure Storage/discrepant_methods.txt", "r")
    discrepant_methods = f.read().split('\n')
    f.close()

    d_count = 0


    # to-do: compare error message when res[0] === false, compare using .response.status_code and response.reason

    with io.StringIO() as buf, redirect_stdout(buf):

        # run blob client ops
        d_count = run_ops(arg["1"], methods_blobClient, "bc", d_count, buf, discrepant_methods)
        # run container client ops
        d_count = run_ops(arg["2"], methods_containerClient, "cc", d_count, buf, discrepant_methods)
        # run blob service client ops
        d_count = run_ops(arg["3"], methods_blobServiceClient, "bsc", d_count, buf, discrepant_methods)
        # run table client ops
        d_count = run_ops(arg["4"], methods_tableClient, "tc", d_count, buf, discrepant_methods)
        # run table service client ops
        d_count = run_ops(arg["5"], methods_tableServiceClient, "tsc", d_count, buf, discrepant_methods)
        # run queue client ops
        d_count = run_ops(arg["6"], methods_queueClient, "qc", d_count, buf, discrepant_methods)
        # run queue service client ops
        d_count = run_ops(arg["7"], methods_queueServiceClient, "qsc", d_count, buf, discrepant_methods)

    with open('../sdk_tests/Azure Storage/discrepancy.txt', 'a') as f:
        f.write(f'{d_count}/{t_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
        f.write('Round ended\n\n')

    # store methods names in order to skip in the next run
    with open('../sdk_tests/Azure Storage/discrepant_methods.txt', 'w') as f:
        f.write("\n".join(discrepant_methods))  

    extract_discrepancy('../sdk_tests/Azure Storage/discrepancy.txt')


'''test suites'''
def main(arg):

    simple_test_run(True)
    # run1v1(arg)
    # run_sequences()


'''Get fuzz data'''
if __name__ == '__main__':
    arg = ()
    main(arg)
    
    


    