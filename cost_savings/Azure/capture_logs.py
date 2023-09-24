import subprocess, os, time, shutil


def run_emulator():

    commands = subprocess.check_output("dotnet test --list-tests", shell=True, text=True) 
    start_index = commands.find("The following Tests are available:") 
    commands = commands[start_index+len("The following Tests are available:"):len(commands)-1]
    commands = [command.strip() for command in commands.split("\n") if command.strip()]

    # Overwrite the new logs instead of appending to the old ones
    dir = os.path.join(os.getcwd(), 'debug_logs')
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)

    for i in commands:

        # create test log file
        # with open(f'{log_folder}/{i}.txt', 'w') as f:
        #     f.write(f"Logs for test: {i}\n\n")
            
        try:
            # Start the emulator process with stdout and stderr redirected to the log file
            # with open(f'./logs/{i}.txt', 'a') as f:
            logpath = f'./debug_logs/' + i 
            emulator_command = ['azurite', '--skipApiVersionCheck', '--debug', logpath]
            emulator_process = subprocess.Popen(emulator_command)   
            
            print(f"Emulator process started for iteration for test: {i}") 

            # ***run dotnet test command with os.system in app path
            os.system(f'dotnet test --filter {i}') 
            
        except Exception as e:
            print(f"Error running test on the emulator: {e}")
        
        finally:
            try:
                # Kill the emulator process
                time.sleep(3)
                emulator_process.terminate()
                while emulator_process.poll() is None:
                    # Process is still running
                    print("Process is running...")
                    
                print(f"Emulator process terminated for test: {i}")
         
            except Exception as e:
                print(f"Error terminating emulator process: {e}")



def main():

    # Set the log file path
    # log_folder = os.path.join(os.getcwd(), 'logs')

    # Run the emulator
    run_emulator()


if __name__ == '__main__':
    main()