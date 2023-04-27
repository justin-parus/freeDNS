import os
import argparse
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

import freeDNS

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(prog="freeDNS",
                                     description="query your ip and send yourself updates")
    parser.add_argument("--webhook", "-w", type=str,
                        help="webhook to post updates")
    parser.add_argument("--email-address", "-e", type=str,
                        help="email address to send updates")
    parser.add_argument("--email-user", "-u", type=str,
                        help="modern smpt requires trust, you need an account to send email")
    parser.add_argument("--email-password", "-p", type=str,
                        help="modern smpt requires trust, you need an account to send email")
    parser.add_argument("--email-server", "-s", type=str, default="smtp.gmail.com:587",
                        help="limit number of processed files. useful for debugging")
    parser.add_argument("--interval-seconds", "-t", type=int, default=300,
                        help="specify number of seconds to check ip")

    args = parser.parse_args()

    dns = freeDNS.FreeDNS(
                    webhook=args.webhook,
                    email_addr=args.email_address,
                    username=args.email_user,
                    password=args.email_password,
                    mail_server=args.email_server)

    scheduler = BlockingScheduler()
    scheduler.add_job(dns.update, "interval", seconds=args.interval_seconds)
    logging.info("Press Ctrl+{0} to exit".format("break" if os.name == "nt" else "c"))

    try:
        logging.info("Starting freeDNS scheduler")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("freeDNS terminated")
