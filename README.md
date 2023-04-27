# freeDNS
query your public ip periodically and udpate if it changes

## update types
 - smpt supprt (with gmail, easily modify for you own)
 - discord webhook

## setup
```bash
python3.10 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pre-commit install
```

### run once to try out
```bash
python src/main.py -e <gmail> -u <gmail-username> -p <app-password>
```

### always run
```bash
sudo cp units/freeDNS.service /etc/systemd/system/
# edit the new service file to replace paths and params
sudo vim /etc/systemd/system/freeDNS.service
sudo systemctl daemon-reload
sudo systemctl enable freeDNS.service
sudo systemctl start freeDNS.service
```

### using gmail
See [App Passwords](https://support.google.com/accounts/answer/185833?visit_id=638181578541975944-1342201244&p=InvalidSecondFactor&rd=1)
set up your own [here](https://myaccount.google.com/apppasswords).
