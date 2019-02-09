# -*- coding: utf-8 -*-
import socket
import sys
import random
import string
import datetime
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer


chatbot = ChatBot('Ron Obvious')
welcomingBool = True
print("set to true")

NUM_TRANSMISSIONS = 100
if (len(sys.argv) < 2):
    print("Usage: python3 " + sys.argv[0] + " server_port")
    sys.exit(1)
assert(len(sys.argv) == 2)
server_port = int(sys.argv[1])
tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.bind(('localhost', server_port))
tcpServer.listen(1)

dinnerIdeas = ["You should just stay home" , "Go get some pizza.", "Make some eggs over easy"]
# TODO: Call accept to wait for a connection
connection, addr = tcpServer.accept()
# Repeat NUM_TRANSMISSIONS times


welcomingMessage = "Hi, I'm Toddy! I can make small talk and also respond to these commands: Joke, Dinner ideas, and Time"


def randJoke():
    joke = "Knock Knock"
    return joke

def dinnerIdea():
    picker = random.randint(0,2)
    return dinnerIdeas[picker]

def currentTime():
    currentDT = datetime.datetime.now()
    time = ("%s:%s and %s seconds :)" % (currentDT.hour, currentDT.minute, currentDT.second))
    return time


def processInput(input):
    if input.lower() == "joke":
        return randJoke()
    elif input.lower() == "math":
        ans = "44"
        return ans
    elif input.lower() == "dinner ideas":
        return dinnerIdea()
    elif input.lower() == "time":
        return currentTime()
    else:
        return chatbot.get_response(input)


for i in range(NUM_TRANSMISSIONS):
    if welcomingBool:
        response = welcomingMessage
        welcomingBool = False
    else:
        data = connection.recv(2000)
        response = processInput(data.decode("utf-8"))

    encResponse = "Toddy:" + str(response)

    encResponse = encResponse.encode()

    connection.sendall(encResponse)

connection.close
