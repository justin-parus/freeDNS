import logging
import requests
import smtplib
import datetime
from typing import Optional
import discordwebhook as dwh

class FreeDNS:
    """Simple DNS Server work-around."""

    def __init__(self,
                 webhook=None,
                 email_addr=None,
                 username=None,
                 password=None,
                 mail_server=None,
                 fail_tolerance=None,
                 timeout=10):
        # other options "http://ident.me", "http://icanhazip.com"
        self.ip_server = "https://api.ipify.org"
        self.last_ip = ""
        self.fail_tolerance = fail_tolerance
        self.fail_count = 0
        self.timeout = timeout

        self.webhook = webhook

        self.password = password
        self.username = username
        self.email_addr = email_addr
        self.mail_server = mail_server

    def update(self):
        msg = self.check_ip()
        if msg:
            if self.webhook:
                self.webhook_ip(msg)
            if (
                    self.email_addr and
                    self.mail_server and
                    self.username and
                    self.password
               ):
                self.mail_ip(msg)

    def webhook_ip(self, ip:str):
        if self.webhook.find("discord") != -1:
            discord = dwh.Discord(url=self.webhook)
            try:
                discord.post(content=f"freeDNS ip update {ip}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to post to {self.webhook} with {e}")

    def mail_ip(self, ip:str):
        email_addr = self.email_addr
        msg = msg = "\r\n".join([
            "From: " + email_addr,
            "To: " + email_addr,
            "Subject: freeDNS ip update",
            "",
            ip
        ])

        try:
            with smtplib.SMTP(self.mail_server) as server:
                server.ehlo()
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(email_addr, email_addr, msg)
            logging.info(f"mailed new ip {ip} to {email_addr}")
        except smtplib.SMTPException as err:
            logging.error(f"failed to mail ip with {err}")

    def reset_fails(self):
        self.fail_count = 0

    def check_fails(self) -> Optional[str]:
        ft = self.fail_tolerance
        if ft:
            self.fail_count += 1
            logging.warning(f"currently at {self.fail_count} failures")
            if self.fail_count > ft:
                self.reset_fails()
                return f"Fail count passed tolerance threshold of {ft}"

        return None

    def check_ip(self) -> Optional[str]:
        logging.info(f"Attempting to check ip at {datetime.datetime.now()}")
        try:
            res = requests.get(self.ip_server, timeout=self.timeout)

            ip = None
            if res.status_code != 200:
                logging.error(f"ip req failed with {res.status_code}")
                return self.check_fails()

            self.reset_fails()
            ip = res.text

            logging.info(f"ip is {ip}")
            if self.last_ip != ip:
                self.last_ip = ip
                return ip
            else:
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get ip with {e}")
            return self.check_fails()
