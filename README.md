## DEFCON Workshop Checker

I missed out on registering for all the cool workshops at DEFCON this year so I whipped this up really quick and deployed it to an aws c2 instance. It ran continuously and checked the sold out registration pages every hour or so and sent me a text message when someone pulled out of a class and a spot was available. :)

Certainly there are better ways to do this, but pretty useful for an hour of work! (also it was fun)

After cloning, you'll need to create a file called `config.py` in the `defcon_workshop_checker` package folder with your Twilio credentials that looks like the following:

```
account_sid = 'your-twilio-acct-sid-goes-between-these-quotes'
auth_token = 'your-twilio-auth_token-goes-between-these-quotes'
to_number = '+1-the-number-sending-to'
from_number = '+1-the-from-number'
```
You'll also need to set an environment variable, which is the link of the main DefCon workshop page, like this:
```
export URL='https://www.defcon.org/html/defcon-25/dc-25-workshops.html'
```
Once `config.py` is saved and your `env` variable it set, just run the following commands to get up and running: 

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python defcon_workshop_checker/defcon_checker.py
```
If you want to run this in the cloud you can spin up a `t2.micro`, `ssh` in, then `git clone`, then follow the instructions above, but before running `python defcon-checker.py`, run the `screen` command, then start the checker, then detach and disconnect from the instance with `ctrl + a, d, d`. Then it will continously run in the background in the cloud. Watch for charges from AWS!
