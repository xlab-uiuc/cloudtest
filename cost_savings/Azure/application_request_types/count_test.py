import json 

def main(): 
    application_name = 'snowmaker.json'

    with open(application_name, "r") as json_file: 
        application_data = json.load(json_file)
    
    test_count = 0 
    for key, val in application_data.items(): 
        if val != {}: 
            test_count += 1 
    
    print("Test Count:", test_count)

main()