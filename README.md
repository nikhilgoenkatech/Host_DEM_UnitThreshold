# Host_DEM_UnitThreshold
A script to configure and trigger an email if the host/dem units exceeds the configured threshold.
There are following files in the package:

# install_dependencies.txt
Install the dependencies and required libraries by running the file as "source install_dependencies.txt"

# config.json
tenant-details: tenant-URL: The tenant URL which will be used to fire the API call
API-token: The API token which will be used to fire the API.
tenant-name: The tenant name.
allocated-host-units: The total number of host units available for that tenant.
threshold-host-units: The threshold (in percentage) post which you would like to be informed by email.
allocated-dem-units: The total DEM units available for that tenant.
threshold-dem-units: The threshold (in percentage) post which you would like to be informed by email.

email-details -
server: The mail-server which will be used to send the email.
port: Port of the mail-server.
username: The username which will be used to login on the smtp-server
password: Password of the SMTP username
senders-list: The sender email-id from which the email-id will be triggered
receivers-list: The recepients email-id who would be alerted
log_file: the log file where the script logs will be saved

# host_threshold.py:
It is a python script that will make API calls to collect information about the current running hosts/user-sessions and their consumption. Once received, it will verify if the current host/dem units consumption has breached the threshold. In case it has breached, it will trigger an email to the configured receipients.

How to run the script:
You can schedule the script to execute as per requirement by using a crontab entry as below: */1 * * * /home/ngoenka/host_threshold.py > host_threshold_out.out
This would run the script every hour and populate/overwrite the excel accordingly.

# Pre-requisites:
For the scripts to run successfully, you would need Python 2.7 running on the server as well as python-pip and pycurl package. You can install pycurl using the following command: sudo apt install python-pycurl and pip using: apt-get python-pip.

# Next steps:
Once the tar file is downloaded, run “source install_dependencies.txt” (executed from the folder where the file install_dependencies.txt is located) – This would install all the libraries required for the script to run successfully.
