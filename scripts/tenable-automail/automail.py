#!/usr/bin/python3

import os
import time
import json
import smtplib
import re
from email.message import EmailMessage
from dotenv import load_dotenv
from tenable.io import TenableIO

load_dotenv()

a_key = os.getenv("ACCESS_KEY")
s_key = os.getenv("SECRET_KEY")
m_user = os.getenv("M_USER")
m_pass = os.getenv("M_PASS")

tio = TenableIO(a_key, s_key)

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
        password=None
):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    msg.set_content(body)

    if cc_email:
        msg['Cc'] = ', '.join(cc_email)
    else:
        cc_email = []

    with open(report_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=report_path)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(username, password)
        server.send_message(msg)

def get_scan_details():
    scans = tio.scans.list()

    formatted = [
            {
                "id": s["id"],
                "name": s["name"]
            }
            for s in scans
    ]
    return print(json.dumps(formatted, indent=4))


def export_scan(scan_id):
    """
        Getting information to make output more readable.
    """
    details = tio.scans.details(scan_id)['settings']
    name = details['name'].replace(" ","_")
    date = time.strftime('%Y%m%d-%H%M%S')
    output_path = f'{date}-{name}_{scan_id}_Report.pdf'

    email_cc = None
    email_to = ""
    email_subject = ""
    email_body = f"""
    Here are the reports for your environment as of {date} for your review.

    This is an automated email. Please do not reply to this email. If you
    need further information or further details please contact 
    <email> or open a ticket.
    """

    print(f" Starting report for {name}....")

    with open(output_path, 'wb') as f:
        tio.scans.export(
                scan_id, 
                format = "pdf",
                chapters = ['vuln_hosts_summary', 'vuln_by_host'],
                fobj=f)

    print(f" Export complete. Saved to {output_path}.\n")

    if re.search(r'.*<ENV>.*\.pdf', output_path):
        print(f'Emailing {output_path} to <ENV> team.')
        email_to = "to@email.com"
        email_cc = ["cc@email.com"]
        email_subject = "Tenable Scan Reports - <ENV> Environment"

    elif re.search(r'.*<ENV>.*\.pdf', output_path):
        print(f'Emailing {output_path} to <ENV> team.')

        email_to = "austin.hamrick@trustcommerce.com"
        email_cc = ["austin.hamrick@spherecommerce.com"]
        email_subject = "Tenable Scan Reports - <ENV> Environment"

    send_report(
           to = email_to,
           sender = "sender@email.com",
           subject = email_subject,
           body = email_body,
           report_path=output_path,
           cc_email = email_cc,
           smtp_server='smtp.mail.com',
           smtp_port='587',
           username=m_user,
           password=m_pass
    )

scan_ids = [140, 149]

for sid in scan_ids:
    export_scan(sid)
