from mitmproxy import http
import subprocess, json 
import utils

REFERENCE_RUN = "False"
CUR_HASHES = {}
HASHES = utils.get_hashes()
ENV = {}

def request(flow: http.HTTPFlow) -> None:
    
   # Capture requests sent to ports 10000, 10001, and 10002
    if flow.request.port in [10000, 10001, 10002]:
        global REFERENCE_RUN
        global CUR_HASHES
        global HASHES
        global ENV

    
        try:
            # a json is sent to set the test and environment
            ENV = json.loads(flow.request.query["message"])
            flow.request.host = "localhost"
            flow.request.port = 80
        except:
            print(f'Current environment: {ENV["env"]}, Current test: {ENV["test"]}')

        # write logs to a file -- these logs are used for cost calculations
        # with open("proxy_logs.txt", "a") as f:
        #     f.write(f'Test: {env["test"]}, Env: {env["env"]}\n')
        #     f.write(f"Captured request to {flow.request.pretty_host}:{flow.request.port}\n")
        #     f.write(f"Request URL: {flow.request.url}\n")
        #     f.write(f"Request Method: {flow.request.method}\n")
        #     f.write(f"Request Headers: {flow.request.headers}\n")
        #     try:
        #         f.write(f"Request Content: {flow.request.text}\n\n")
        #     except:
        #         pass

        # check if its a test complete ping
            if "message" in flow.request.query and flow.request.query["message"] == "complete_run":

                if ENV['test'] in CUR_HASHES:
                    if ENV['test'] in HASHES and HASHES[ENV['test']] != CUR_HASHES[ENV['test']]:
                            REFERENCE_RUN = "True"
                            print(f'Hash mismatch! Reference run')
                    else:
                        HASHES[ENV['test']] = CUR_HASHES[ENV['test']]
                    
                    CUR_HASHES = {}
                    
                flow.request.host = "localhost"
                flow.request.port = 80
                utils.set_seed(0)
                utils.reset_replacement_dict()
            
            elif "message" in flow.request.query and flow.request.query["message"] == "complete_reference_run":  # we skip resetting the hashes and keep the default cloud hashes in the reference run

                if ENV['test'] in CUR_HASHES:
                    HASHES[ENV['test']] = CUR_HASHES[ENV['test']]
                    CUR_HASHES = {}

                REFERENCE_RUN = "False"

                flow.request.host = "localhost"
                flow.request.port = 80
                utils.set_seed(0)
                utils.reset_replacement_dict()

            elif "message" in flow.request.query and flow.request.query["message"] == "tests_complete":
                flow.request.host = "localhost"
                flow.request.port = 80
                utils.save_hashes(HASHES)

            else:
                
                cur_hash = utils.hash_request(flow.request)

                if ENV['test'] in CUR_HASHES:
                    CUR_HASHES[ENV['test']].append(cur_hash)
            
                else:
                    CUR_HASHES[ENV['test']] = [cur_hash]


                if ENV['env'] == "emulator":
                    if flow.request.port == 10000:
                        flow.request.port = 20000
                    elif flow.request.port == 10001:
                        flow.request.port = 20001
                    elif flow.request.port == 10002:
                        flow.request.port = 20002

                    flow.request.host = "localhost"


                elif ENV['env'] == "cloud":
                    # load config
                    config = utils.load_config()

                    key = ""

                    if flow.request.port == 10000:
                        flow.request.host = config['cloud_host_blob']
                        key = subprocess.run(['az', 'account', 'get-access-token','--resource',f'https://{config["cloud_host_blob"]}'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()[2].replace('"','').replace(',','')
                    elif flow.request.port == 10001:
                        flow.request.host = config['cloud_host_queue']
                        key = subprocess.run(['az', 'account', 'get-access-token','--resource',f'https://{config["cloud_host_queue"]}'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()[2].replace('"','').replace(',','')
                    elif flow.request.port == 10002:
                        flow.request.host = config['cloud_host_table']
                        key = subprocess.run(['az', 'account', 'get-access-token','--resource',f'https://{config["cloud_host_table"]}'], stdout=subprocess.PIPE).stdout.decode('utf-8').split()[2].replace('"','').replace(',','')
                    
                    flow.request.scheme = "https"
                    flow.request.port = 443  # Set the port for HTTPS
                    flow.request.url = flow.request.url.replace('devstoreaccount1/', '')
                    
                    # TO-DO: Customize the access token command based on the cloud provider
                    
                    flow.request.headers['Authorization'] = f'Bearer {key}'
                    
                    # update body                    
                    try:
                        flow.request.text = flow.request.text.replace("http://127.0.0.1:10000/devstoreaccount1", "https://sdkfuzz.blob.core.windows.net")
                        flow.request.text = flow.request.text.replace("http://127.0.0.1:10001/devstoreaccount1", "https://sdkfuzz.queue.core.windows.net")
                        flow.request.text = flow.request.text.replace("http://127.0.0.1:10002/devstoreaccount1", "https://sdkfuzz.table.core.windows.net")
                        flow.request.text = flow.request.text.replace("127.0.0.1", "sdkfuzz.core.windows.net")
                    except:
                        pass





    

def response(flow: http.HTTPFlow) -> None:
    
    if "message" in flow.request.query and (flow.request.query["message"] == "complete_run" or flow.request.query["message"] == "complete_reference_run"):
        global REFERENCE_RUN
        flow.response.headers["reference-run"] = str(REFERENCE_RUN)
        REFERENCE_RUN = "False"
    



