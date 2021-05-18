import os
import json
import datetime
import time
import pync
import sys


def parseTime(time):

    numberTime = time.split(" ")[0]
    day = time.split(" ")[1]
    hour = numberTime[len(numberTime)-2:]
    timeExact = numberTime[0:len(numberTime)-2]
    print(day)
    print(hour)
    print(timeExact)
    today = datetime.date.today().strftime("%d-%m-%Y").split("-")
    if hour == "pm":
        epoch = int((datetime.datetime(int(today[2]), int(today[1]), int(today[0]), int(timeExact.split(
            ":")[0])+12, int(timeExact.split(":")[1])) - datetime.datetime(1970, 1, 1)).total_seconds())
    else:
        epoch = int((datetime.datetime(int(today[2]), int(today[1]), int(today[0]), int(timeExact.split(
            ":")[0]), int(timeExact.split(":")[1])) - datetime.datetime(1970, 1, 1)).total_seconds())
    if day == "tomorrow":
        epoch += 86400
    print(epoch)
    return epoch//60


class Reminder:

    def __init__(self,  file):
        mode = 'r+' if os.path.exists(file) else 'a+'
        self.fileName = file
        file = open(file, mode)
        try:
            self.data = json.loads(file.readline())
        except:
            self.data = {}
        print(type(self.data))
        file.close()

    def add(self, time, message):
        try:
            self.data[parseTime(time)].append(message)
        except:
            self.data[parseTime(time)] = [message]
        print(self.data)
        file = open(self.fileName, "r+")
        file.truncate(0)
        file.write(json.dumps(self.data))

    def getReminderToday(self):
        pass

    def printAll(self):
        print(self.data)

    def triggerNotification(self):
        currentTime = int(time.time())//60
        if str(currentTime) in self.data:
            for message in self.data[str(currentTime)]:
                pync.notify(message)
        else:
            pync.notify("no current reminder !!!!!")


def run(typeRun):
    reminder = Reminder("reminder.txt")
    if typeRun == "trigger":
        reminder.triggerNotification()
    elif typeRun == "add":
        userTime = str(input("Enter time to be reminded : "))
        userMessage = str(input("Enter message to be reminded : "))
        reminder.add(userTime, userMessage)
        print("your reminder is successfully added :)")


if __name__ == "__main__":
    typeRun = sys.argv[1]
    print(typeRun)
    run(typeRun)
