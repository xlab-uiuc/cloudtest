import os, json
result = {}
for filename in os.listdir(os.getcwd()):
   if filename.endswith(".json"):
    with open(os.path.join(os.getcwd(), filename), 'r') as f:
        data = json.loads(f.read())
        for key in data.keys():
            for item in data[key]:
                if item not in result:
                    result[item] = 0
                result[item] += 1
# Add extra durabletask in different format
with open("durable_task_operations_result", "r") as f:
   data = json.loads(f.read())
   for key in data.keys():
    if key not in result:
        result[key] = 0
    result[key] += data[key] 
print(result)
print(len(result))        
print(json.dumps(result, indent=4))