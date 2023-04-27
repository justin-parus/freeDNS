# freeDNS
query your public ip periodically and udpate if it changes

## update types
 - smpt supprt (with gmail, easily modify for you own)
 - discord webhook

## usage
```bash
# use tmux, screen, bg or something more reliable like systemd
python src/main.py -e <gmail> -u <gmail-username> -p <app-password>
```

### using gmail
See [App Passwords](https://support.google.com/accounts/answer/185833?visit_id=638181578541975944-1342201244&p=InvalidSecondFactor&rd=1)
set up your own [here](https://myaccount.google.com/apppasswords).

## dev
```bash
python3.10 -m venv venv
pip install -r requirements.txt
pre-commit install
```
