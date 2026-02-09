import requests
import selectorlib
import smtplib, ssl
import time
import sqlite3

URL = "https://darshit2714.github.io/webScrap/"
class Event:
    def scrape(self, url):
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value
class Email:
    def send_mail(self, message):
        host = "smtp.gmail.com"
        port = 465
        username = "xyz@gmail.com"
        password = "***************"
        receiver = "abc@gmail.com"
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username,receiver,message)
            print("Mail sent successfully")
class Database:
    def __init__(self): # constructor function in python
        self.connection = sqlite3.connect("data.db")
    def store(self,extracted):
        # with open("event.txt","a") as file:
        #     file.write(extracted + "\n")
        row = extracted.split(",")
        row = [i.strip() for i in row]
        cursor = self.connection.cursor()
        cursor.execute("insert into events values(?,?,?)", row)
        self.connection.commit()
    def read(self,extracted):
        # with open("event.txt","r") as file:
        #     return file.read()
        row = extracted.split(",")
        row = [i.strip() for i in row]
        cursor = self.connection.cursor()
        event,city,date = row
        cursor.execute("select * from events where event=? and city=? and date=?",(event,city,date))
        row = cursor.fetchall()
        print(row)
        return row
if __name__ == "__main__":
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)
        if extracted != 'No upcoming event':
            db = Database()  # it will call constructor function _init_
            content = db.read(extracted)
            if not content:
                db.store(extracted)
                mail = Email()
                mail.send_mail(message="You have a new event in your city.")
        time.sleep(10)