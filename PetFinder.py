import argparse
import smtplib
import ssl
import time

import requests
import schedule
from lxml import html

global argument
global global_pets


def job():
    try:
        print("checking pets")
        global global_pets
        current_pets = fetch_pets()

        if current_pets != global_pets:
            email(current_pets)
            global_pets = current_pets
    except:
        print("failed")


def fetch_pets():
    global argument
    page = requests.get(argument.url)
    tree = html.fromstring(page.content)
    animals = tree.xpath(
        '//*[@id="paragraph-230"]/div/div/div/div/div/div[2]/div/div[@class="col-md-4 col-xl-3 mb-5 views-row"]/article/h2/a/span/text()')
    times = tree.xpath(
        '//*[@id="paragraph-230"]/div/div/div/div/div/div[2]/div/div[@class="col-md-4 col-xl-3 mb-5 views-row"]/article/h2/a/text()')
    pets = []
    for i in range(len(animals)):
        pets.append(animals[i] + ' ' + times[i].strip().strip('\\n'))
    return pets


def email(pets):
    context = ssl.create_default_context()
    global argument
    message = str(pets).strip('[]')
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        print("sending email " + message)
        server.login(argument.sender, argument.password)
        server.sendmail(argument.sender, argument.receiver, message)


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Description for my parser")
        parser.add_argument("-u", "--url",
                            help="Scottish SPCA URL for pets. Example: https://www.scottishspca.org/rehome/rehome-find-a-pet?type%5B30%5D=30",
                            required=True, default="")
        parser.add_argument("-s", "--sender", help="Sender gmail address", required=True, default="")
        parser.add_argument("-p", "--password", help="Sender gmail password", required=True, default="")
        parser.add_argument("-r", "--receiver", help="Receiver gmail address", required=True, default="")

        global argument
        argument = parser.parse_args()

        global global_pets
        global_pets = [""]
        schedule.every(5).seconds.do(job)
        while 1:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    app = CommandLine()
