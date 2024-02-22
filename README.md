# Secure Firewall Offline Updater

## Overview
This tool is a work in progress effort example to pull offline update packages for Cisco Secure Firewall and store them in a remote server directory,

### Note
Please be aware this project is a proof of concept and is not expected to be used as a production application without due diligence.

## Requirements

1. API credentials to Cisco Secure Firewall Management Center
2. Compute resource with python3 installed

## Configuration

1. Clone the repository into the desired directory
2. cd into the cloned directory
3. Install dependencies, ```pip install -r requirements.txt```
4. Run the following command with associated arguments:

```bash
python3 fmc_offline_updater.py --server SCP_IP_HOSTNAME --user admin --password PASSWORD --directory /scp --minimum_version 7.2
```

Arguments: 
* --server, Hostname or IP of FMC
* --user, IP or hostname of the SCP server
* --password, Password for authenticating with SCP Server
* --directory, Full directory path of the SCP server
* --minimum_version, Lowest version number to pull updates for *Defaults to 6.4*
* --log_name, Name of log file to write *Defaults to logs*
* --log_directory, Directory path to write log file *Defaults to ./logs*
