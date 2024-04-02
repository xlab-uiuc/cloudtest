from contextlib import redirect_stdout
from .containerclient import ContainerClient
from .blobclient import MyBlobClient
from .blobserviceclient import MyBlobServiceClient
from .blobleaseclient import MyBlobLeaseClient
from azure.core.exceptions import HttpResponseError
import io, random, json
import itertools

BEHAVIOR_MISMATCH_COUNT = 0
ERROR_MISMATCH_COUNT = 0
STATUS_CODE_MISMATCH_COUNT = 0

config = json.loads(open('config.json').read())

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
    with open('logs/azure_blob/unique_discrepancy.txt', 'a') as f:
        f.write('\n\n'.join(li))


def initialize_clients():
    cloud_objects = {}
    em_objects = {}

    # random blob, container name
    blob_name = f'blob{random.randint(1,100000)}'
    container_name = f'container{random.randint(1,100000)}'

    cloud_objects['bc'] = MyBlobClient(False, container_name, blob_name)
    em_objects['bc'] = MyBlobClient(True, container_name, blob_name)
    cloud_objects['cc'] = ContainerClient(False, container_name, blob_name)
    em_objects['cc'] = ContainerClient(True, container_name, blob_name)
    cloud_objects['bsc'] = MyBlobServiceClient(False, container_name, blob_name)
    em_objects['bsc'] = MyBlobServiceClient(True, container_name, blob_name)
    cloud_objects['blc'] = MyBlobLeaseClient(False, container_name, blob_name)
    em_objects['blc'] = MyBlobLeaseClient(True, container_name, blob_name)

    return cloud_objects, em_objects

def outcome(flag):
    if flag:
        return 'SUCCESS'
    else:
        return 'FAILURE'


def oracles(res_cloud, res_em):
    log = ''
    flag =  False
    global BEHAVIOR_MISMATCH_COUNT
    global ERROR_MISMATCH_COUNT
    global STATUS_CODE_MISMATCH_COUNT

    # # check exception nature for 2nd and 3rd oracle
    # # https://learn.microsoft.com/en-us/python/api/azure-core/azure.core.exceptions?view=azure-python
    # if not res_cloud[0] and isinstance(res_cloud[1], HttpResponseError):
    #     if not res_em[0] and isinstance(res_em[1], HttpResponseError):
    #         httpException = True

    if res_cloud[0] == res_em[0] and res_em[0] == True:
        return flag, ""

    elif res_cloud[0] != res_em[0]:
        flag = True
        log += (f'--Behavior mismatch--\n')
        log += (f'CLOUD: {outcome(res_cloud[0])} -- Response: {res_cloud[1]} \n')
        log += (f'EMULATOR: {outcome(res_em[0])} -- Response: {res_em[1]}\n\n ')
        BEHAVIOR_MISMATCH_COUNT += 1
        return flag, log

    cloud_code = res_cloud[1].response.status_code
    em_code = res_em[1].response.status_code
    cloud_msg = res_cloud[1].response.reason
    em_msg = res_em[1].response.reason

    if cloud_code != em_code:
        flag = True
        log += (f'--Status code mismatch--\n')
        log += (f'CLOUD: {outcome(res_cloud[0])} -- Error Code: {cloud_code} -- Error Message: {cloud_msg}\n')
        log += (f'EMULATOR: {outcome(res_em[0])} -- Error Code: {em_code} -- Error Message: {em_msg}\n\n ')
        STATUS_CODE_MISMATCH_COUNT += 1

    elif cloud_msg != em_msg:
        flag = True
        log += (f'--Error message mismatch--\n')
        log += (f'CLOUD: {outcome(res_cloud[0])}  -- Error Message: {cloud_msg}\n')
        log += (f'EMULATOR: {outcome(res_em[0])} -- Error Message: {em_msg}\n\n ')
        ERROR_MISMATCH_COUNT += 1

    return flag, log
        


def run_ops(arg, methods, client, count, discrepant_methods):

    t_count = -1
    for method in methods:
            t_count += 1
            
            # to increase fuzzing efficiency however it trades off coverage
            # if method.__name__ in discrepant_methods:
            #     continue

            # we make a new client in order to run an operation independently
            if client == "bc":
                test_cloud = MyBlobClient(False)
                test_em = MyBlobClient()
            elif client == "cc":
                test_cloud = ContainerClient(False)
                test_em = ContainerClient()
            elif client == "bsc":
                test_cloud = MyBlobServiceClient(False)
                test_em = MyBlobServiceClient()
            elif client == "blc":
                test_cloud = MyBlobLeaseClient(False)
                test_em = MyBlobLeaseClient()

            try:
                print('\nMETHOD: '+ method.__name__, '--- ARGS: ',arg[t_count])

                if not arg[t_count] == None:
                    # run method on cloud and emulator
                    res_cloud = method(test_cloud, arg[t_count])
                    res_em = method(test_em, arg[t_count])

                    # oracles
                    result = oracles(res_cloud, res_em)
                    
                    if result[0]:
                        count += 1
                        print('\nDISCREPANCY FOUND!\n')
                        print(result[1])

                        if method.__name__ not in discrepant_methods:
                            discrepant_methods.append(method.__name__)

                        with open('logs/azure_blob/discrepancy.txt', 'a') as f:
                            f.write(f'DISCREPANT METHOD: {method.__name__} --- ARGS: {arg[t_count]}\n')
                            f.write(result[1])
                            f.write(f'\n\n\ncount: {count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
            
            except Exception as e:
                print("Exception: ", e)

            finally:
                test_cloud.__cleanup__()
                test_em.__cleanup__()

    return count


# to-do: implement type

def run_sequences(methods, type, runs):

    global BEHAVIOR_MISMATCH_COUNT
    global ERROR_MISMATCH_COUNT
    global STATUS_CODE_MISMATCH_COUNT

    BEHAVIOR_MISMATCH_COUNT = 0
    ERROR_MISMATCH_COUNT = 0
    STATUS_CODE_MISMATCH_COUNT = 0

    d_count = 0
    t_count = runs

    with io.StringIO() as buf, redirect_stdout(buf):

        if type == 'shuffle':
            discrepant_seqs, d_count = run_sequences_shuffle(methods, runs)
        elif type == 'permutation':
            discrepant_seqs, d_count, t_count = run_sequences_permutation(methods)

        # store methods names in order to skip in the next run
        with open('logs/azure_blob/discrepant_sequences.txt', 'a') as f:
            f.write("\n".join(discrepant_seqs))  

        output = buf.getvalue().strip()

    # write buf to a new file
    with open('logs/azure_blob/log_all.txt', 'a') as f:
        f.write(output)

    with open('logs/azure_blob/discrepancy.txt', 'a') as f:
        f.write('***  Sequences Run Summary  ***\n\n')
        f.write(f'Behavior mismatch count: {BEHAVIOR_MISMATCH_COUNT}\n')
        f.write(f'Status code mismatch count: {STATUS_CODE_MISMATCH_COUNT}\n')
        f.write(f'Error message mismatch count: {ERROR_MISMATCH_COUNT}\n')
        f.write(f'Total discrepancy count: {d_count}/{t_count}\n\n\n')


def run_sequences_permutation(methods):

    d_count = 0
    t_count = 0
    discrepant_seq = []
    methods_list = methods['bc'] + methods['cc'] + methods['bsc'] + methods['blc']
    list_seqs = list(itertools.combinations(methods_list, 5))

    counter = 0
    while counter < len(list_seqs):

        cloud_objects, em_objects = initialize_clients()
        t_count += 1
        print(f'\n\nTEST SEQUENCE: [{", ".join(i.__name__ for i in list_seqs[counter])}]\n')
        
        sublist = []

        for method in list_seqs[counter]:
            sublist.append(method)
            print('METHOD: '+ method.__name__, '--- ARGS: []')
            if method in methods['bc']:
                result = oracles(method(cloud_objects['bc'], []), method(em_objects['bc'], []))
            elif method in methods['cc']:
                result = oracles(method(cloud_objects['cc'], []), method(em_objects['cc'], []))
            elif method in methods['bsc']:
                result = oracles(method(cloud_objects['bsc'], []), method(em_objects['bsc'], []))
            elif method in methods['blc']:
                result = oracles(method(cloud_objects['blc'], []), method(em_objects['blc'], []))

            if result[0]:    
                d_count += 1
                print('\nDISCREPANCY FOUND!\n')
                print(f'{result[1]}\n\n')

                discrepant_seq.append(f'{d_count}: [{", ".join(i.__name__ for i in sublist)}]')

                with open('logs/azure_blob/discrepancy.txt', 'a') as f:
                    f.write(f'DISCREPANT METHOD: {method.__name__} --- ARGS: []\n')
                    f.write(result[1])
                    f.write(f'\n\n\ncount: {d_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
        
                list_seqs = list_seqs[:counter+1] + [list_seqs[i] for i in range(counter, len(list_seqs)) if not check_sublist_in_list(list(list_seqs[i]), sublist)]
                break
        
        counter += 1

        with open('logs/azure_blob/discrepancy.txt', 'a') as f:
            f.write(f'\nSEQUENCE COMPLETE   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

        # delete all objects
        for key in cloud_objects:
            cloud_objects[key].__cleanup__()
            em_objects[key].__cleanup__()
        

    return discrepant_seq, d_count, t_count


def run_sequences_shuffle(methods, runs):
    
    d_count = 0
    discrepant_seq = []
    discrepant_method = []

    for _ in range(runs):

         # randomize seed
        seed = random.randint(0, 1000000)

        # shuffle args -- we dont fuzz args in sequence fuzzing
        # for i in arg.items():
        #     random.Random(seed).shuffle(i[1])

        # shuffle all methods
        random.Random(seed).shuffle(methods['bc'])
        random.Random(seed).shuffle(methods['cc'])
        random.Random(seed).shuffle(methods['bsc'])
        random.Random(seed).shuffle(methods['blc'])

        methods_list = methods['bc'] + methods['cc'] + methods['bsc'] + methods['blc'] 

        cloud_objects, em_objects = initialize_clients()

        print(f'\n\nTEST SEQUENCE: [{", ".join(i.__name__ for i in methods_list[:7])}]\n')
        sublist = []
        
        for method in methods_list[:7]:
            sublist.append(method)
            print('METHOD: '+ method.__name__, '--- ARGS: []')
            if not method.__name__ in discrepant_method:
                if method in methods['bc']:
                    result = oracles(method(cloud_objects['bc'], []), method(em_objects['bc'], []))
                elif method in methods['cc']:
                    result = oracles(method(cloud_objects['cc'], []), method(em_objects['cc'], []))
                elif method in methods['bsc']:
                    result = oracles(method(cloud_objects['bsc'], []), method(em_objects['bsc'], []))
                elif method in methods['blc']:
                    result = oracles(method(cloud_objects['blc'], []), method(em_objects['blc'], []))

                if result[0]:    
                    d_count += 1
                    print('\nDISCREPANCY FOUND!\n')
                    print(f'{result[1]}\n\n')
                    discrepant_method.append(method.__name__)

                    discrepant_seq.append(f'{d_count}: [{", ".join(i.__name__ for i in sublist)}]')

                    with open('logs/azure_blob/discrepancy.txt', 'a') as f:
                        f.write(f'DISCREPANT METHOD: {method.__name__} --- ARGS: []\n')
                        f.write(result[1])
                        f.write(f'\n\n\ncount: {d_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
                    break

        with open('logs/azure_blob/discrepancy.txt', 'a') as f:
            f.write(f'SEQUENCE COMPLETE   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

        # delete all objects
        for key in cloud_objects:
            cloud_objects[key].__cleanup__()
            em_objects[key].__cleanup__()

    return discrepant_seq, d_count


def run1v1(arg, methods, t_count):

    global BEHAVIOR_MISMATCH_COUNT
    global ERROR_MISMATCH_COUNT
    global STATUS_CODE_MISMATCH_COUNT

    BEHAVIOR_MISMATCH_COUNT = 0
    ERROR_MISMATCH_COUNT = 0
    STATUS_CODE_MISMATCH_COUNT = 0

    # do not run discrepant methods again
    f = open("logs/azure_blob/discrepant_methods.txt", "r")
    discrepant_methods = f.read().split('\n')
    f.close()

    d_count = 0

    # done --> to-do: compare error message when res[0] === false, compare using .response.status_code and response.reason

    with io.StringIO() as buf, redirect_stdout(buf):

        # run blob client ops
        d_count = run_ops(arg["1"], methods['bc'], "bc", d_count, discrepant_methods)
        # run container client ops
        d_count = run_ops(arg["2"], methods['cc'], "cc", d_count, discrepant_methods)
        # run blob service client ops
        d_count = run_ops(arg["3"], methods['bsc'], "bsc", d_count, discrepant_methods)
        # run blob lease client ops
        d_count = run_ops(arg["4"], methods['blc'], "blc", d_count, discrepant_methods)

        output = buf.getvalue().strip()


    with open('logs/azure_blob/discrepancy.txt', 'a') as f:
        f.write(f"Round discrepancies: {d_count}\n")
        f.write('***  Overall Summary  ***\n\n')
        f.write(f'Behavior mismatch count: {BEHAVIOR_MISMATCH_COUNT}\n')
        f.write(f'Status code mismatch count: {STATUS_CODE_MISMATCH_COUNT}\n')
        f.write(f'Error message mismatch count: {ERROR_MISMATCH_COUNT}\n')
        f.write(f'Total discrepancy count: {BEHAVIOR_MISMATCH_COUNT + STATUS_CODE_MISMATCH_COUNT + ERROR_MISMATCH_COUNT}/{t_count}\n\n\n')

    with open('logs/azure_blob/discrepancy.txt', 'a') as f:
        f.write(f'ROUND ENDED   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

    # store methods names in order to skip in the next run
    with open('logs/azure_blob/discrepant_methods.txt', 'a') as f:
        f.write("\n".join(discrepant_methods))  

    # write buf to a new file
    with open('logs/azure_blob/log_all.txt', 'a') as f:
        f.write(output)


'''test suites'''
def main(arg):

    methods = {}
    # get all methods of all the clients
    methods['bc'] = [getattr(MyBlobClient, attr) for attr in dir(MyBlobClient) if callable(getattr(MyBlobClient, attr)) and not attr.startswith("__")]
    methods['cc'] = [getattr(ContainerClient, attr) for attr in dir(ContainerClient) if callable(getattr(ContainerClient, attr)) and not attr.startswith("__")]
    methods['bsc'] = [getattr(MyBlobServiceClient, attr) for attr in dir(MyBlobServiceClient) if callable(getattr(MyBlobServiceClient, attr))
     and not attr.startswith("__")]
    methods['blc'] = [getattr(MyBlobLeaseClient, attr) for attr in dir(MyBlobLeaseClient) if callable(getattr(MyBlobLeaseClient, attr)) and not attr.startswith("__")]
    total_methods = methods['bc'] + methods['cc'] + methods['bsc'] + methods['blc'] 
    t_count = len(total_methods)
    # logging.basicConfig(level=logging.DEBUG)


    # empty args for default run of ops
    if arg == ():
        arg = {}
        arg['1'] = [[]] * len(methods['bc'])
        arg['2'] = [[]] * len(methods['cc'])
        arg['3'] = [[]] * len(methods['bsc'])
        arg['4'] = [[]] * len(methods['blc'])

    else:
        assert len(arg) == 4, "Invalid number of clients"
        assert len(arg['1']) == len(methods['bc']), "Invalid number of methods for BlobClient"
        assert len(arg['2']) == len(methods['cc']), "Invalid number of methods for ContainerClient"
        assert len(arg['3']) == len(methods['bsc']), "Invalid number of methods for BlobServiceClient"
        assert len(arg['4']) == len(methods['blc']), "Invalid number of methods for BlobLeaseClient"


    # take the number of sequences as input
    global config
    c = int(config['sequence_length'])
    type_fuzz = config['fuzz_type']

    run1v1(arg, methods, t_count)
    run_sequences(methods, type_fuzz, c)



'''Get fuzz data'''
if __name__ == '__main__':
    arg = ()
    main(arg)
    
    


    