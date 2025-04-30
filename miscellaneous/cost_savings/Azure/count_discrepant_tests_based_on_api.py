import json 

def getAPIList(file_name):
    api_names = [] 
    with open(file_name, 'r') as file: 
        for line in file: 
            api_name = line.strip()
            if api_name not in api_names: # It won't be, sanity check
                api_names.append(api_name)
    
    return api_names

def getdiscrepantTests(file_path, discrepant_APIs):
    with open(file_path, 'r') as file: 
        data = json.load(file) 

    discrepant_tests = [] 
    disc_apis = [] 
    for test, apis in data.items(): 
        for api in apis: 
            if api in discrepant_APIs: 
                disc_apis.append(api)
                discrepant_tests.append(test)
                break 
        
    return discrepant_tests, discrepant_APIs

def main(): 
    discrepant_emulator_APIs = getAPIList('./discrepantApisEmulator.txt')
    discrepant_tests, discrepant_apis = getdiscrepantTests('./application_sdk_methods/orleans.json', discrepant_emulator_APIs)

    # print(alpakka_discrepant_tests)
    print(f"Number of tests: {len(discrepant_tests)}")
    print(f"Discrepant APIs: {discrepant_apis}")

if __name__ == "__main__": 
    main()  