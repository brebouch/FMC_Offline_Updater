#############################################################
#                                                           #
# FMC Offline Updater                                       #
# Author: Brennan Bouchard                                  #
#                                                           #
# Date: 2/22/24                                             #
#                                                           #
#############################################################
import os
import xmltodict
import requests
import argparse
import time
import paramiko
import log

parser = argparse.ArgumentParser(description='Cisco FMC Offline Updater')
parser.add_argument('--server', help='IP or hostname of the SCP server',
                    required=False, default='localhost')
parser.add_argument('--directory', help='Full directory path of the SCP server',
                    required=False, default='./scp')
parser.add_argument('--user', help='Username for authenticating to the SCP server',
                    required=False, default=None)
parser.add_argument('--password', help='Password for authenticating to the SCP server',
                    required=False, default=None)
parser.add_argument('--minimum_version', help='Lowest version number to pull updates for',
                    required=False, default='6.4')
parser.add_argument('--log_name', help='Name of log file to write',
                    required=False, default='logs')
parser.add_argument('--log_directory', help='Name directory path for the log file',
                    required=False, default='./logs')

args = parser.parse_args()
logger = log.get_logger(log_name=f'{args.log_name}.log', log_path=args.log_directory)

images_base_url = 'https://cdo-ftd-images.s3-us-west-2.amazonaws.com'


def scp_file(file_name):
    try:
        logger.debug(f'Attempting to SCP file {file_name} to {args.server}/{args.directory}')
        ssh = paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(args.server, username=args.user, password=args.password)
        sftp = ssh.open_sftp()
        local_file = f'./scp/{file_name}'
        if os.path.isfile(local_file):
            sftp.chdir(args.directory)
            sftp.put(local_file, f'{args.directory}/{file_name.split("/")[1]}')
            sftp.close()
            ssh.close()
            logger.debug(f'Successfully copied file {file_name} to {args.server}/{args.directory}')
            return True
    except Exception as e:
        logger.debug(f'Unable to copy file {file_name} to {args.server}/{args.directory}')
        logger.debug(f'Exception: {e}')
        return False


def check_remote_files(file_name):
    try:
        logger.debug(f'Checking remote directory {args.server}/{args.directory} for file {file_name}')
        ssh = paramiko.SSHClient()
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.connect(args.server, username=args.user, password=args.password)
        sftp = ssh.open_sftp()
        sftp.chdir(args.directory)
        files = sftp.listdir()
        sftp.close()
        ssh.close()
        if file_name in files:
            logger.debug(f'File {file_name} already exists on {args.server}/{args.directory}')
            return True
        logger.debug(f'File {file_name} does not exist on {args.server}/{args.directory}')
        return False
    except Exception as e:
        logger.debug(f'Unable to search for file {file_name} on {args.server}/{args.directory}')
        logger.debug(f'Exception: {e}')
        return False


def get_xml_images():
    logger.debug('Collecting list of available FTD Images')
    resp = requests.get(f'{images_base_url}/cdoFtdImages.xml')
    if resp.status_code == 200:
        return xmltodict.parse(resp.content)
    logger.debug('Unable to pull list of FTD images, HTTP status code: ' + str(resp.status_code))


def get_support_files():
    logger.debug('Collecting list of available support files')
    resp = requests.get(f'{images_base_url}/supportFiles.xml')
    if resp.status_code == 200:
        logger.debug('Successfully pulled list of available support files')
        return xmltodict.parse(resp.content)
    logger.debug('Unable to pull list of available support files, HTTP status code: ' + str(resp.status_code))


def check_update_version(ver):
    minimum = args.minimum_version.split('.')
    check = ver.split('.')
    if int(check[0]) >= int(minimum[0]):
        if int(check[1]) >= int(minimum[1]):
            return True


def get_updates():
    files = get_support_files()
    for f in files['support_files']['file']:
        if '_VDB_' in f['file_name'] or '_GEODB_' in f['file_name'] or check_update_version(f['requires']):
            if not check_remote_files(f['file_name']):
                get_file(f['file_path'])


def get_file(file_name):
    logger.debug('Getting file: ' + file_name)
    resp = requests.get(f'{images_base_url}/{file_name}')
    if resp.status_code == 200:
        logger.debug('File GET successful, saving to local directory')
        file_writer = open(f'./scp/{file_name}', 'wb')
        file_writer.write(resp.content)
        file_writer.close()
        logger.debug('File written, copying to remote directory')
        time.sleep(.2)
        scp_file(file_name)
        delete_local_file(file_name)
    else:
        logger.debug('File GET failed, HTTP status code: ' + str(resp.status_code))


def delete_local_file(file_name):
    logger.debug('Cleaning up local file: ' + file_name)
    os.remove(f'./scp/{file_name}')


if __name__ == '__main__':
    logger.debug('Starting FMC Offline Updater, this service will poll for updates every 5 minutes, enter Crtl+C to exit')
    while True:
        get_updates()
        time.sleep(300)

