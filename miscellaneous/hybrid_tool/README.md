# Hybrid Testing Tool

## Installing Dependencies

### mitmproxy
Install mitmproxy by following the instructions provided in their official documentation:
[mitmproxy Installation Guide](https://docs.mitmproxy.org/stable/overview-installation/)

### socat
Install socat using your package manager (e.g., apt for Ubuntu, brew for macOS):
```bash
sudo apt install socat  # For Ubuntu
brew install socat      # For macOS
```
### azure-cli
```bash
sudo apt-get install -y azure-cli   # For Ubuntu
brew install azure-cli              # For macOS
```



## Directing Traffic using socat

To direct traffic from ports 10000, 10001, and 10002 to port 8080 using socat, run the following commands:
```bash
socat TCP-LISTEN:10000,fork TCP:localhost:8080
socat TCP-LISTEN:10001,fork TCP:localhost:8080
socat TCP-LISTEN:10002,fork TCP:localhost:8080
```
## Configuration

1. **Set Default Test Environment:**
    - Ensure tests are configured to run by default on the emulator.

2. **Define Cloud Host URL:**
    - Specify the cloud host URL for routing traffic to the cloud environment in `config.json`.

3. **Cloud Authentication:**
    - Provide an authentication token generation command for establishing cloud authentication in `proxy.py` (will be moved to config.json soon - ignore for now).

4. **Test Directory Path:**
    - Specify the test directory path within your project in `config.json`.

5. **List All Tests Command:**
    - Define a command to list all available tests in `run_tests.py` (will be moved to config.json soon - ignore for now).

6. **Framework:**
    - Define dotnet framework if there is a specific one you want to use.

## Starting mitmproxy

Start mitmproxy by running the script proxy.py with the following command:
```bash
mitmdump -s proxy.py
```

## Running Azurite

To run Azurite, use the following command:
```bash
azurite --blobPort 20000 --queuePort 20001 --tablePort 20002 --skipApiVersionCheck
```

## Running the Tool Across Commits

To run the tool across commits, execute the run_commits.py script using Python:
```bash
python run_commits.py
```