from mitmproxy import http
import subprocess, json 
import utils

REFERENCE_RUN = "False"

# TO-DO: Remove and test frequent writes to cur_hashes


def request(flow: http.HTTPFlow) -> None:
   # Capture requests sent to ports 10000, 10001, and 10002
    if flow.request.port in [10000, 10001, 10002]:
        global REFERENCE_RUN

        CUR_HASHES = utils.get_cur_hashes()

        # check environment variable to determine if the request should be sent to the emulator or cloud run
        env = utils.load_env()
        print(f'Current environment: {env["env"]}')

        # write logs to a file
        with open("proxy_logs.txt", "a") as f:
            f.write(f'Test: {env["test"]}, Env: {env["env"]}\n')
            f.write(f"Captured request to {flow.request.pretty_host}:{flow.request.port}\n")
            f.write(f"Request URL: {flow.request.url}\n")
            f.write(f"Request Method: {flow.request.method}\n")
            f.write(f"Request Headers: {flow.request.headers}\n")
            try:
                f.write(f"Request Content: {flow.request.text}\n\n")
            except:
                pass

        # check if its a test complete ping
        if "message" in flow.request.query and flow.request.query["message"] == "complete_run":

            if env['test'] in CUR_HASHES:
                HASHES = utils.get_hashes()
                if env['test'] in HASHES and HASHES[env['test']] != CUR_HASHES[env['test']]:
                        REFERENCE_RUN = "True"
                        print('3')
                        print(f'Hash mismatch! Reference run')
                else:
                    HASHES[env['test']] = CUR_HASHES[env['test']]
                    utils.save_hashes(HASHES)
                
                utils.save_cur_hashes({})
                
            flow.request.host = "localhost"
            flow.request.port = 80
        
        elif "message" in flow.request.query and flow.request.query["message"] == "complete_reference_run":  # we skip resetting the hashes and keep the default cloud hashes in the reference run

            if env['test'] in CUR_HASHES:
                HASHES = utils.get_hashes()
                HASHES[env['test']] = CUR_HASHES[env['test']]
                utils.save_hashes(HASHES)
                utils.save_cur_hashes({})
            
            REFERENCE_RUN = "False"

            flow.request.host = "localhost"
            flow.request.port = 80

        else:
            
            cur_hash = utils.hash_request(flow.request)

            if env['test'] in CUR_HASHES:
                CUR_HASHES[env['test']].append(cur_hash)
                utils.save_cur_hashes(CUR_HASHES)
                print('2')
         
            else:
                CUR_HASHES[env['test']] = [cur_hash]
                utils.save_cur_hashes(CUR_HASHES)
                print('1')


            if env['env'] == "emulator":
                if flow.request.port == 10000:
                    flow.request.port = 20000
                elif flow.request.port == 10001:
                    flow.request.port = 20001
                elif flow.request.port == 10002:
                    flow.request.port = 20002

                flow.request.host = "localhost"
                    # print(f'New request: {flow.request.pretty_host}:{flow.request.port}')
                
            elif env['env'] == "cloud":
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
                # print(flow.request.url)
                
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



        
            # write forwarded request to proxy_logs.txt
            with open("proxy_logs.txt", "a") as f:
                f.write(f"Forwarded request to {flow.request.pretty_host}:{flow.request.port}\n")
                f.write(f"Request URL: {flow.request.url}\n")
                f.write(f"Request Method: {flow.request.method}\n")
                f.write(f"Request Headers: {flow.request.headers}\n")
                try:
                    f.write(f"Request Content: {flow.request.text}\n\n")
                except:
                    pass


    

def response(flow: http.HTTPFlow) -> None:
    
    if "message" in flow.request.query and (flow.request.query["message"] == "complete_run" or flow.request.query["message"] == "complete_reference_run"):
        global REFERENCE_RUN
        flow.response.headers["reference-run"] = str(REFERENCE_RUN)
        REFERENCE_RUN = "False"
        
    env = utils.load_env()
    # write logs to a file
    with open("responses.txt", "a") as f:
        f.write(f'Test: {env["test"]}, Env: {env["env"]}\n')
        f.write(f"Captured response from {flow.request.pretty_host}:{flow.request.port}\n")
        f.write(f"Request URL: {flow.request.url}\n")
        f.write(f"Request Method: {flow.request.method}\n")
        f.write(f"Response Status Code: {flow.response.status_code}\n")
        f.write(f"Response Headers: {flow.response.headers}\n")
        try:
            f.write(f"Response Content: {flow.response.text}\n\n")
        except:
            pass


