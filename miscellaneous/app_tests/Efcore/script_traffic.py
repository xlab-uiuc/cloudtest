import subprocess
import os
import time
import signal
# f = open("sniff.txt", "w")
# p = subprocess.Popen(['C:\\Program Files\\Wireshark\\tshark.exe',
#                       '-i',
#                       'Adapter for loopback traffic capture'],
#                  stdout=f,
#                  )
seen = {}
with open("tests.txt", "r", encoding='utf16') as tests, open("result.txt", "w", encoding='utf-8') as result, open("log", "w", encoding='utf-8') as log:
    for line in tests:
        test = str(line.strip())
        state = 0
        test_without_bracket = ""
        for c in test:
            if state == 0 and c == '(':
                state = 1
            elif state == 0:
                test_without_bracket += c
            elif state == 1 and c == ')':
                state = 0
        if test_without_bracket in seen.keys():
            continue
        else:
            seen[test_without_bracket] = 0
        cmd = f"dotnet test --filter \"{test_without_bracket}\" > null"
        print("Running " + cmd)
        f = open("sniff.txt", "w", encoding='utf-8')
        old_size = os.path.getsize("sniff.txt")
        print(f"old size is: {old_size}")
        p = subprocess.Popen(['C:\\Users\\anna\\Downloads\\WiresharkPortable64\\App\\Wireshark\\tshark.exe',
                      '-i',
                      'Adapter for loopback traffic capture',
                      '-f',
                      'tcp port 8081'],
                 stdout=f,
                 stderr=subprocess.DEVNULL
        )
        os.system(cmd)
        p.send_signal(signal.SIGTERM)
        p.wait()
        f.close()
        traffic = False
        log.write(f"\n---{test}---\n")
        new_size = os.path.getsize("sniff.txt")
        print(f"new size is {new_size}")
        if (os.path.getsize("sniff.txt") > old_size):
            result.write(f"{test_without_bracket}: True\n")
        else:
            result.write(f"{test_without_bracket}: False\n")
        
        # try:
        #     with open('sniff.txt', 'r', encoding='utf-8') as f:
        #         for line in f:
        #             log.write(line)
        #             if "8081" in line:
        #                 traffic = True
        #         result.write(f"{test_without_bracket}: {traffic}\n")
        # except:
        #     print("Exception")
        #     log.write(f"Exception {test_without_bracket}")
        result.flush()
        log.flush()