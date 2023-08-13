import os 
import json 
import chardet 

def applicationData(applicationName): 
    current_dir = os.getcwd() 
    traffic_path = os.path.join(current_dir, applicationName) 
    file_names = os.listdir(traffic_path) 

    application_json_object = {} 
    for file_name in file_names: 
        total_head = 0 
        total_patch = 0 
        total_puts = 0 
        total_gets = 0 
        total_post = 0 
        total_delete = 0 
        total_other = 0 
        unit_test_data = {} 

        with open(os.path.join(traffic_path, file_name), "r", encoding='UTF-8') as file: 
            for line in file: 
                single_line = line.strip()
                components = single_line.split()

                if len(components) > 0: 
                    if components[0] == '127.0.0.1': 
                        req_type = components[5][1:]
                        match req_type: 
                            case "PUT": 
                                total_puts += 1 
                            case "GET":
                                total_gets += 1
                            case "POST": 
                                total_post += 1 
                            case "DELETE": 
                                total_delete += 1
                            case "PATCH": 
                                total_patch += 1 
                            case "HEAD": 
                                total_head += 1 
                            case _: 
                                total_other += 1  

            unit_test_data['PUT'] = total_puts 
            unit_test_data['GET'] = total_gets 
            unit_test_data['POST'] = total_post 
            unit_test_data['DELETE'] = total_delete 
            unit_test_data['PATCH'] = total_patch 
            unit_test_data['HEAD'] = total_head
            unit_test_data['OTHER'] = total_other 

        application_json_object[file_name] = unit_test_data 
    return application_json_object  

def saveJSONObject(applicationName, applicationData):
    current_dir = os.getcwd() 
    file_name = applicationName + ".json" 
    file_path = os.path.join(current_dir, file_name) 
    with open(file_path, "w") as json_file: 
        json.dump(applicationData, json_file, indent=4) 

def main(): 
    current_dir = os.getcwd() 
    applications = [application for application in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, application))]

    for application in applications: 
        app_data = applicationData(application)
        saveJSONObject(application, app_data) 



main()