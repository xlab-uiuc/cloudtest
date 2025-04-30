# Eᴛ

The following is the guideline on how to run Eᴛ. The logs and the subsequent calculations of the savings can be found in [cost_savings](../cost_savings/).

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

Install azure-cli which is used tp integrate authentication of azure APIs with Eᴛ.

```bash
sudo apt-get install -y azure-cli   # For Ubuntu
brew install azure-cli              # For macOS
```

## Directing Traffic to proxy

To direct traffic from ports 10000, 10001, and 10002 to port 8080 using socat, run the following commands:

```bash
socat TCP-LISTEN:10000,fork TCP:localhost:8080
socat TCP-LISTEN:10001,fork TCP:localhost:8080
socat TCP-LISTEN:10002,fork TCP:localhost:8080
```

## Configuration

We have pre-defined the configurations in `config.json` specific to each project.

// TODO: Need to add a link to the artifacts that show how to configure projects to point to the emulator.

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
