import os 
import json 
import chardet 

def getRequestTypes(traffic_path, file_names):  
    application_req_types = {} 
    for file_name in file_names: 
        unit_test_data = {} 

        with open(os.path.join(traffic_path, file_name), "r", encoding='UTF-8') as file: 
            for line in file: 
                single_line = line.strip()
                components = single_line.split()

                if len(components) > 6: 
                    if components[6].find('RequestHeaders') != -1 and components[6].find('user-agent') != -1: 
                        user_agent_index = components[6].index('user-agent')
                        user_agent = components[6][user_agent_index+13:].split()[0]
                        # print(user_agent)

                        if user_agent not in unit_test_data.keys(): 
                            unit_test_data[user_agent] = {'PUT':0, 'GET':0, 'POST':0, 'DELETE':0, 'HEAD':0, 'PATCH':0, 'OTHER': 0}

                        if components[4].find('RequestMethod') != 1: 
                            req_type = components[4][len('RequestMethod='):]
                            # print(req_type)
                            match req_type: 
                                case "PUT": 
                                    unit_test_data[user_agent]['PUT'] += 1
                                case "GET":
                                    unit_test_data[user_agent]['GET'] += 1
                                case "POST":
                                    unit_test_data[user_agent]['POST'] += 1 
                                case "DELETE": 
                                    unit_test_data[user_agent]['DELETE'] += 1
                                case "PATCH": 
                                    unit_test_data[user_agent]['PATCH'] += 1
                                case "HEAD": 
                                    unit_test_data[user_agent]['HEAD'] += 1
                                case _: 
                                    unit_test_data[user_agent]['OTHER'] += 1
        application_req_types[file_name] = unit_test_data 
    return application_req_types  

def getAPICalls(traffic_path, file_names):
    application_api_calls = {} 
    for file_name in file_names: 
        unit_test_api_calls = [] 
        with open(os.path.join(traffic_path, file_name), "r", encoding='UTF-8') as file: 
            for line in file:
                single_line = line.strip()  
                components = single_line.split() 

                if len(components) > 3: 
                    if components[3] == 'DispatchMiddleware:': 
                        if components[4].find('Operation=') != -1: 
                            api_call = components[4][len('Operation='):]
                            if api_call not in unit_test_api_calls: 
                                unit_test_api_calls.append(api_call)
        application_api_calls[file_name] = unit_test_api_calls
    return application_api_calls


def saveJSONObject(applicationName, applicationData):
    current_dir = os.getcwd() 
    file_name = applicationName + ".json" 
    file_path = os.path.join(current_dir, file_name) 
    with open(file_path, "w") as json_file: 
        json.dump(applicationData, json_file, indent=4) 

def main(): 
    applicationName = 'attachmentplugin'
    current_dir = os.getcwd() 
    traffic_path = os.path.join(current_dir, applicationName) 
    file_names = os.listdir(traffic_path)

    app_data = getRequestTypes(traffic_path, file_names)
    saveJSONObject('../application_req_types/attachmentplugin', app_data)

    api_calls = getAPICalls(traffic_path, file_names)
    saveJSONObject('../sdk_methods/attachmentplugin', api_calls)


main()