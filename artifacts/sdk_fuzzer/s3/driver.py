from contextlib import redirect_stdout
import io, json
import random
from .s3client import S3Client


BEHAVIOR_MISMATCH_COUNT = 0
ERROR_MISMATCH_COUNT = 0
STATUS_CODE_MISMATCH_COUNT = 0

config = json.loads(open('config.json').read())

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

    if res_cloud[0] == res_em[0] and res_em[0] == True:
        return flag, ""

    elif res_cloud[0] != res_em[0]:
        flag = True
        log += (f'--Behavior mismatch--\n')
        log += (f'CLOUD: {outcome(res_cloud[0])} -- Response: {res_cloud[1]} \n')
        log += (f'EMULATOR: {outcome(res_em[0])} -- Response: {res_em[1]}\n\n')
        BEHAVIOR_MISMATCH_COUNT += 1
        return flag, log

    cloud_code = res_cloud[1].response['Error']['Code']
    em_code = res_em[1].response['Error']['Code']
    cloud_msg = res_cloud[1].response['Error']['Message']
    em_msg = res_em[1].response['Error']['Message']
    cloud_http = res_cloud[1].response['ResponseMetadata']['HTTPStatusCode']
    em_http = res_em[1].response['ResponseMetadata']['HTTPStatusCode']
    
    if cloud_http != em_http:
        flag = True
        log += (f'--Status code mismatch--\n')
        log += (f'CLOUD: {outcome(res_cloud[0])} -- HTTP Status code: {cloud_http} -- Error Code: {cloud_code} -- Error Message: {cloud_msg}\n')
        log += (f'EMULATOR: {outcome(res_em[0])} -- HTTP Status code: {em_http} -- Error Code: {em_code} -- Error Message: {em_msg}\n\n')
        STATUS_CODE_MISMATCH_COUNT += 1

    elif cloud_msg != em_msg:
        flag = True
        log += (f'--Error message mismatch--\n')
        log += (f'CLOUD: {outcome(res_cloud[0])}  -- Error Message: {cloud_msg} -- Error Code: {cloud_code} -- HTTP Status code: {cloud_http}\n')
        log += (f'EMULATOR: {outcome(res_em[0])} -- Error Message: {em_msg} -- Error Code: {em_code}\n\n -- HTTP Status code: {em_http}')
        ERROR_MISMATCH_COUNT += 1

    return flag, log



def run_ops(arg, methods, count, discrepant_methods):

    t_count = -1
    for method in methods:
            t_count += 1
            
            # to increase fuzzing efficiency however it trades off coverage
            # if method.__name__ in discrepant_methods:
            #     continue

            test_cloud = S3Client(False)
            test_em = S3Client()
           
            try:
                print(f'METHOD: {method.__name__} --- ARGS: {arg[t_count]}')

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

                    with open('logs/s3/discrepancy.txt', 'a') as f:
                    # with open('discrepancy.txt', 'a') as f:
                        f.write(f'DISCREPANT METHOD: {method.__name__} --- ARGS: {arg[t_count]}\n')
                        f.write(result[1])
                        f.write(f'\n\ncount: {count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
            
            except Exception as e:
                print("Exception: ", e)

            finally:
                test_cloud.__cleanup__()
                test_em.__cleanup__()

    return count


def run1v1(arg, methods_s3, t_count):

    global BEHAVIOR_MISMATCH_COUNT
    global ERROR_MISMATCH_COUNT
    global STATUS_CODE_MISMATCH_COUNT

    # do not run discrepant methods again
    f = open("logs/s3/discrepant_methods.txt", "r")
    discrepant_methods = f.read().split('\n')
    f.close()

    discrepant_methods = []

    d_count = 0

    with io.StringIO() as buf, redirect_stdout(buf):

        # run S3 client ops
        d_count = run_ops(arg["1"], methods_s3, d_count, discrepant_methods)
        
        output = buf.getvalue().strip()

    with open('logs/s3/discrepancy.txt', 'a') as f:
        f.write(f"Round discrepancies: {d_count}\n")
        f.write('***  Overall Summary  ***\n\n')
        f.write(f'Behavior mismatch count: {BEHAVIOR_MISMATCH_COUNT}\n')
        f.write(f'Status code mismatch count: {STATUS_CODE_MISMATCH_COUNT}\n')
        f.write(f'Error message mismatch count: {ERROR_MISMATCH_COUNT}\n')
        f.write(f'Total discrepancy count: {BEHAVIOR_MISMATCH_COUNT + STATUS_CODE_MISMATCH_COUNT + ERROR_MISMATCH_COUNT}/{t_count}\n\n\n')



    with open('logs/s3/discrepancy.txt', 'a') as f:
        f.write(f'Round ended   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

    # store methods names in order to skip in the next run
    with open('logs/s3/discrepant_methods.txt', 'a') as f:
        f.write("\n".join(discrepant_methods))  

    # extract_discrepancy('logs/s3/discrepancy.txt')

    # write buf to a new file
    with open('logs/s3/log_all.txt', 'w') as f:
        f.write(output)


def run_sequences_shuffle(methods, runs):
    
    d_count = 0
    discrepant_seq = []
    discrepant_method = []

    for _ in range(runs):

         # randomize seed
        seed = random.randint(0, 1000000)

        # shuffle methods
        random.Random(seed).shuffle(methods)

        cloud_object = S3Client(False)
        em_object = S3Client()

        print(f'\n\nTEST SEQUENCE: [{", ".join(i.__name__ for i in methods[:7])}]\n')
        sublist = []
        
        for method in methods[:7]:
            sublist.append(method)
            print('METHOD: '+ method.__name__, '--- ARGS: []')
            if not method.__name__ in discrepant_method:

                result = oracles(method(cloud_object, []), method(em_object, []))

                if result[0]:    
                    d_count += 1
                    print('\nDISCREPANCY FOUND!\n')
                    print(f'{result[1]}\n\n')
                    discrepant_method.append(method.__name__)

                    discrepant_seq.append(f'{d_count}: [{", ".join(i.__name__ for i in sublist)}]')

                    with open('logs/s3/discrepancy.txt', 'a') as f:
                        f.write(f'DISCREPANT METHOD: {method.__name__} --- ARGS: []\n')
                        f.write(result[1])
                        f.write(f'\n\n\ncount: {d_count}   ------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')
                    break

        with open('logs/s3/discrepancy.txt', 'a') as f:
            f.write(f'SEQUENCE COMPLETE   ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n\n\n')

       
        cloud_object.__cleanup__()
        em_object.__cleanup__()

    return discrepant_seq, d_count


'''test suites'''
def main(arg):
    # get methods
    methods_s3 = [getattr(S3Client, attr) for attr in dir(S3Client) if callable(getattr(S3Client, attr)) and not attr.startswith("__")]
    t_count = len(methods_s3)

    if arg == ():
        arg = {}
        arg['1'] = [[]] * len(methods_s3)
    else:
        assert len(arg['1']) == len(methods_s3), "Invalid number of methods"
    
    global config
    c = int(config['sequence_length'])

    run1v1(arg, methods_s3, t_count)
    run_sequences_shuffle(methods_s3, c)

'''Get fuzz data'''
if __name__ == '__main__':
    arg = ()
    main(arg)