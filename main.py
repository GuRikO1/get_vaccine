import os
import logging
import time
from datetime import datetime, timedelta, timezone
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
import slackweb


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
logger.propagate = False

url = os.environ['TARGET_URL']
JST = timezone(timedelta(hours=+9), 'JST')

options = ChromeOptions()
options.add_argument('--headless')
options.add_argument("--no-sandbox")
driver = Chrome(options=options)

slack = slackweb.Slack(url=os.environ['SLACK_WEBHOOK_URL'])


def send_to_slack(text):
    slack.notify(text=text)


def main():
    while True:
        logger.info(f'INFO: [{datetime.now(JST)}] Start watching website {url}')
        send_flag = False
        send_text = f'予約TOP: {url}\n\n'
        driver.get(url)
        driver.implicitly_wait(10)
        preserve_links = driver.find_elements_by_partial_link_text("午")
        
        logger.info(f'INFO: [{datetime.now(JST)}] Get reservation info')

        for a in preserve_links:
            day_url = a.get_attribute("href")
            date = day_url.split('date=')[1].split('&')[0]

            r = requests.get(day_url)
            soup = BeautifulSoup(r.content, "html.parser")
            alert = soup.select_one('div.alert')

            res_frame = date + ' ' + a.text
            if not alert:
                note = f'* {res_frame}: 予約が可能です\n\t{url}: {day_url}'
                send_text += note + '\n'
                logger.info(note)
                send_flag = True
            elif '満杯' not in alert.get_text():
                note = f'* {res_frame}: 予約が可能です\n\t{url}: {day_url}'
                send_text += note + '\n'
                logger.info(note)
                send_flag = True
            else:
                note = f'* {res_frame}: 予約が満杯です'
                logger.info(note)

        if send_flag:
            logger.info(f'INFO: [{datetime.now(JST)}] Send below message to slack')
            logger.info(send_text)
            send_to_slack(send_text)
        
        logger.info(f'INFO: [{datetime.now(JST)}] Stop watching website')
        time.sleep(300)
 

if __name__ == '__main__':
    main()
