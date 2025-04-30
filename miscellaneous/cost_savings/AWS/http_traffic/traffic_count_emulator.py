import os 
import json 

def getAPICalls(traffic_path, file_names):
    application_api_calls = {} 
    for file_name in file_names: 
        unit_test_api_calls = [] 

        with open(os.path.join(traffic_path, file_name), "r") as file: 
            for line in file: 
                single_line = line.strip() 
                components = single_line.split() 

                if len(components) > 7: 
                    if components[7] == "AWS": 
                        api = components[8].split(".")[1]
                        if api not in unit_test_api_calls: 
                            unit_test_api_calls.append(api)

        application_api_calls[file_name] = unit_test_api_calls

    return application_api_calls

def saveJSONObject(applicationName, applicationData):
    current_dir = os.getcwd() 
    file_name = applicationName + ".json" 
    file_path = os.path.join(current_dir, file_name) 
    with open(file_path, "w") as json_file: 
        json.dump(applicationData, json_file, indent=4) 

def main(): 
    applicationName = './Orleans'
    current_dir = os.getcwd() 
    traffic_path = os.path.join(current_dir, applicationName) 
    file_names = os.listdir(traffic_path)

    api_calls = getAPICalls(traffic_path, file_names)
    saveJSONObject('./Orleans', api_calls)

if __name__ == "__main__": 
    main() 