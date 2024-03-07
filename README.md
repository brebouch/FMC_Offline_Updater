# Secure Firewall Offline Updater

## Overview
This tool is a work in progress effort example to pull offline update packages for Cisco Secure Firewall and store them in a remote server directory

### Note
Please be aware this project is a proof of concept and is not expected to be used as a production application without due diligence.

## Requirements

1. Linux server hosting directory for SCP files
2. Credentials to access Linux server with appropriate directory permissions
3. Compute resource with python3 installed

## Configuration

1. Clone the repository into the desired directory
2. cd into the cloned directory
3. Install dependencies, ```pip install -r requirements.txt```
4. Run the following command with associated arguments:

```bash
python3 fmc_offline_updater.py --content_update_url "https://example-url.com" --image_update_url "https://example-url.com" --server SCP_IP_HOSTNAME --user admin --password PASSWORD --directory /scp --minimum_version 7.2
```

Arguments: 
* --content_update_url, url for pulling dynamic content update files
* --image_update_url, url for pulling dynamic image update files
* --server, Hostname or IP of FMC
* --user, IP or hostname of the SCP server
* --password, Password for authenticating with SCP Server
* --directory, Full directory path of the SCP server
* --minimum_version, Lowest version number to pull updates for *Defaults to 6.4*
* --log_name, Name of log file to write *Defaults to logs*
* --log_directory, Directory path to write log file *Defaults to ./logs*
