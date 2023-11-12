import os

GET_LOG_CMD = "localstack logs > logs.txt"

os.system(GET_LOG_CMD)
prev_size = os.path.getsize("./logs.txt")

tests_tigger_traffic = []

with open("./tests.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        test_name = str(line).strip()
        os.system(f"dotnet test --filter {test_name} > /dev/null 2>&1")
        print("Process " + test_name)
        os.system(GET_LOG_CMD)
        cur_size = os.path.getsize("./logs.txt")
        if cur_size > prev_size:
            prev_size = cur_size
            tests_tigger_traffic.append(test_name)

print(f"{len(tests_tigger_traffic)} tests trigger traffic in the emulator")
print(tests_tigger_traffic)

with open("./test_with_traffic.txt", "w") as f:
    for test in tests_tigger_traffic:
        f.write(f"{test}\n")