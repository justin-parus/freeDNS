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
                 mail_server=None):
        # other options "http://ident.me", "http://icanhazip.com"
        self.ip_server = "https://api.ipify.org"
        self.last_ip = ""

        self.webhook = webhook

        self.password = password
        self.username = username
        self.email_addr = email_addr
        self.mail_server = mail_server

    def update(self):
        ip = self.check_ip()
        if ip:
            if self.webhook:
                self.webhook_ip(ip)
            if (
                    self.email_addr and
                    self.mail_server and
                    self.username and
                    self.password
               ):
                self.mail_ip(ip)

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

    def check_ip(self) -> Optional[str]:
        logging.info(f"Attempting to check ip at {datetime.datetime.now()}")
        try:
            ip = requests.get(self.ip_server).text

            if ip is not None:
                logging.info(f"ip is {ip}")
                if self.last_ip != ip:
                    self.last_ip = ip
                    return ip
                else:
                    return None
            else:
                logging.error("ip is none")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to get ip with {e}")
            return None
