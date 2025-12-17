# Tenable Auto-Mailer
## What does it do?
 This script is currently set to run on a schedule of every day at 12:30 PM PT.
 It grabs certain scans based on the scan IDs and then emails them to their perspective parties.
 It utilizes pytenable to communicate with the TenableIO API to automate the email of reports 
 as well as export, and gather information about them.

## Functions
```python
def send_report(
        to, 
        sender,
        subject,
        body,
        report_path,
        cc_email=None,
        smtp_server='',
        smtp_port='587',
        username=None,
        password=None) 
```
This function was built to email the reports to the end users. It is built off of <i>EmailMessage</i> module.

```python
def get_scan_details():
```
This function is built as a helper function for getting different information about the scans.
It retrieves information such as the scan ID and the scan name.

```python
def export_scan(scan_id)
```
This function is really the meat of the script. It has the logic to decide who to send the report to.
It also functions to download the report, read the report, and launch the export through the Tenable
API.
