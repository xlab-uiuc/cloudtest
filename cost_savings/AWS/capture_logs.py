import subprocess, os, time


def run_emulator(log_folder):

    # ***run dotnet list command with os.system in app_path and capture test names in li
    commands = subprocess.check_output("dotnet test --list-tests", shell=True, text=True) 
    start_index = commands.find("The following Tests are available:") 
    commands = commands[start_index+len("The following Tests are available:"):len(commands)-1]
    commands = [command.strip() for command in commands.split("\n") if command.strip()]

    # Create the log folder if it doesn't exist
    os.makedirs(log_folder, exist_ok=True)
    # os.makedirs(os.path.join(os.getcwd(), 'debug_logs'), exist_ok=True)

    for i in commands:

        # create test log file
        with open(f'{log_folder}/{i}.txt', 'w') as f:
            f.write(f"Logs for test: {i}\n\n")
            
        try:
            # Start the emulator process with stdout and stderr redirected to the log file
            with open(f'./logs/{i}.txt', 'a') as f:
                emulator_command = ['localstack', 'start']
                emulator_process = subprocess.Popen(emulator_command, stdout=f, stderr=f)   
            
            print(f"Emulator process started for iteration for test: {i}") 

            # ***run dotnet test command with os.system in app path
            os.system(f'dotnet test --filter {i}') 
            
        except Exception as e:
            print(f"Error running test on the emulator: {e}")
        
        finally:
            try:
                # Kill the emulator process
                time.sleep(3)
                os.system('docker stop localstack_main') 
                emulator_process.terminate()
                print(f"Emulator process terminated for test: {i}")
         
            except Exception as e:
                print(f"Error terminating emulator process: {e}")



def main():

    # Set the log file path
    log_folder = os.path.join(os.getcwd(), 'logs')

    # Run the emulator
    run_emulator(log_folder)


if __name__ == '__main__':
    main()