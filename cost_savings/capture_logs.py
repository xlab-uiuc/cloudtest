import subprocess, os, time


def run_emulator(emulator_command, log_folder, app_path):

    # ***run dotnet list command with os.system in app_path and capture test names in li
    li = ['test1', 'test2', 'test3']

    # Create the log folder if it doesn't exist
    os.makedirs(os.path.dirname(log_folder), exist_ok=True)

    for i in li:

        # create test log file
        with open(f'{log_folder}/{i}.txt', 'w') as f:
            f.write(f"Logs for test: {i}\n\n")
            
        try:
            # Start the emulator process with stdout and stderr redirected to the log file
            with open(f'{log_folder}{i}.txt', 'a') as f:
                emulator_process = subprocess.Popen(emulator_command, stdout=f, stderr=f)   
            
            print(f"Emulator process started for iteration for test: {i}") 

            # ***run dotnet test command with os.system in app path
            
        except Exception as e:
            print(f"Error running test on the emulator: {e}")
        
        finally:
            try:
                # Kill the emulator process
                time.sleep(3)
                emulator_process.terminate()
                print(f"Emulator process terminated for test: {i}")
         
            except Exception as e:
                print(f"Error terminating emulator process: {e}")



def main():
    
    # Set the command
    emulator_command = "azurite"

    # *app is a variable
    # Set the log file path
    log_folder = "app/logs/"

    # Set app path
    app_path = "app/"

    # Run the emulator
    run_emulator(emulator_command, log_folder, app_path)


if __name__ == '__main__':
    main()