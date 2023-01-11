# Importing Libraries

from bs4 import BeautifulSoup
import requests
import time
import datetime
import csv
import smtplib
import ssl
from email.message import EmailMessage

#############################################################################################################

# Sending yourself an email when a price hits below a certain level that interests you

def email_sender():
    # Define email sender and receiver
    email_sender = 'EMAIL@gmail.com'
    email_password = 'PASSWORD'
    email_receiver = 'EMAIL@ANYTHING.com'

    # Set the subject and body of the email
    subject = 'The Watch you want is below 2,000.00 Dhs! Now is your chance to buy!'
    body = """
    Ahmad Amine, This is the moment we have been waiting for. Now is your chance to pick up the watch of your dreams. Don't mess it up! Link here: https://www.jumia.ma/watch-4-classic-46-mm-black-samsung-mpg1169626.html
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

#############################################################################################################


def check_price():

    # Connecting to Amazon T-shirt page and pulling in data

    URL = 'https://www.jumia.ma/watch-4-classic-46-mm-black-samsung-mpg1169626.html'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.27", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")

    # a lil bit of formatting

    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(class_='-fs20 -pts -pbxs').get_text()

    price = soup2.find(class_='-b -ltr -tal -fs24').get_text()

    # Cleaning Data

    price = price.replace(' Dhs', '')
    price = price.replace(',', '')
    price = price.strip()
    title = title.strip()

    # Creating a Timestamp for your output to track when data was collected

    today = datetime.date.today()

    # Writing headers and data into the file

    header = ['Title', 'Price', 'Date']
    data = [title, price, today]

    # Appending data to the csv

    with open('dataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

    if(float(price) < 4000.00):
        email_sender()
        print("Email Sent Successfuly")

#############################################################################################################

# Runing check_price after 24h and inputs data into your CSV

while(True):
    check_price()
    time.sleep(10)