import os 
import json 

def applicationData(applicationName): 
    current_dir = os.getcwd() 
    traffic_path = os.path.join(current_dir, applicationName) 
    file_names = os.listdir(traffic_path) 

    application_json_object = {} 
    for file_name in file_names: 
        total_puts = 0 
        total_gets = 0 
        total_post = 0 
        total_delete = 0 
        unit_test_data = {} 
        client_assembly_list = [] 
        with open(os.path.join(traffic_path, file_name), "r", encoding='UTF-16') as file: 
            for line in file: 
                single_line = line.strip()
                components = single_line.split()

                if len(components) > 0: 
                    if components[0] == '[Informational]': 
                        if components[2] == 'Request': 
                            type_of_request = components[4]
                            if type_of_request == 'GET': 
                                total_gets += 1 
                            elif type_of_request == 'POST': 
                                total_post += 1 
                            elif type_of_request == 'PUT': 
                                total_puts += 1 
                            elif type_of_request == 'DELETE': 
                                total_delete += 1 
                    elif components[0] == 'client': 
                        if components[1] == 'assembly:':
                            if components[2] not in client_assembly_list: 
                                client_assembly_list.append(components[2]) 

            unit_test_data['assemblies'] = client_assembly_list 
            unit_test_data['PUT'] = total_puts 
            unit_test_data['GET'] = total_gets 
            unit_test_data['POST'] = total_post 
            unit_test_data['DELETE'] = total_delete 

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