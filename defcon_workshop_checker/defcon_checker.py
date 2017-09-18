# This script finds defcon workshop links and checks each of them to see
# if they're sold out. If one is open, you get a text message with a 
# link to the registration page so you can get the open spot!!1

import requests, time, threading, os, config
from bs4 import BeautifulSoup, SoupStrainer
from twilio.rest import Client
from datetime import datetime

URL = os.environ.get('URL') or 'https://www.defcon.org/html/defcon-25/dc-25-workshops.html'
SECONDS_BETWEEN_CHECKS = 3600 # seconds between checking batch of all links

# twilio account credentials
account_sid = config.account_sid
auth_token = config.auth_token

# set up twilio client with above credentials
client = Client(account_sid, auth_token)

# function to get links to check for status
def getDefConLinks():  
  print('\n*** Gathering links to check... ***\n')
  regList = []
  # collect registration links to check for openings
  res = requests.get(URL)
  res.raise_for_status()

  for link in BeautifulSoup(res.text, 'html.parser', parse_only=SoupStrainer('a')):
    if link.has_attr('href'):
      if link.text.startswith('https://dc25_'):
        regList.append(link.text)
  print('\n*** Links saved to array ***\n')
  return regList

# function to grab sold out status of each link
def checkLinksForStatus(linkList, messageArray):

  # request initial link
  res1 = requests.get(linkList)

  # get final redirect of above url (to eventbrite reg page)
  res2 = res1.url

  # scrape contents of final url direct page
  # there's probably a better way to do this
  res3 = requests.get(res2)
  defcon = BeautifulSoup(res3.text, "html.parser")

  # grab div with "Sold Out" info in it
  soldOut = defcon.select('.listing-panel-info__price-or-status')
    
  # get text from above div
  soldOutText = soldOut[0].getText()
 
  # check for "S" in "Sold Out"
  if soldOutText[10] == 'S':
    print(res2[29:70] + ' Sold Out' + ' ' + str(datetime.now().time()) + '\n')
  else:
    for link in messageArray:
      if linkList == link:
        break
      else:
        messageArray.append(linkList)
        print(res2[29:70] + ' seems to be open!!!!!!!1111!!!1\n')

        # this section sends a text message if a spot is open
        message = client.api.account.messages.create(to=config.to_number,
                                         from_=config.from_number,
                                         body="Register NOW!!! test " + linkList)

def main():
  # get all links to workshops, done only once
  regList = getDefConLinks()
  downloadThreads = []
  alreadyMessaged = []
  counter = 0

  print('\nStarting to check for open spots...\n')
  # loop to check for open spots
  while True:
    print('total batch checks: ' + str(counter) + '\n')
  
    # takes reglist and splits each item (approx 30) into its own thread
    for i in range(0, len(regList)):
      downloadThread = threading.Thread(target=checkLinksForStatus,\
                                  args=[regList[i], alreadyMessaged])
      downloadThreads.append(downloadThread)
      downloadThread.start()
  
    # waits until all threads are completed before moving on
    for downloadThread in downloadThreads:
      downloadThread.join()
    print('\nwaiting ' + str(SECONDS_BETWEEN_CHECKS/60) + ' minutes dot dot dot...\n')
  
    # waits set amount of time before re-checking and increments counter for logging
    time.sleep(SECONDS_BETWEEN_CHECKS)
    counter += 1

if __name__ == '__main__':
  main()
