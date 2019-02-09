from socket import AF_INET, socket, SOCK_STREAM
import tkinter
from threading import Thread
import sys
import time

def receive():
    while True:
        received_reply = clientSock.recv(1024).decode("utf8")
        time.sleep(1) #delays the printing of the reply from server to give it a flow
        msg_list.insert(tkinter.END, received_reply)


def send(event=None):  # binders use event. They pass the data for event
    msg = my_msg.get()
    sentmsg = "Me:"+msg
    msg_list.insert(tkinter.END,sentmsg)
    my_msg.set("")  # Clears input field.
    clientSock.send(bytes(msg, "utf8"))


def exited(event=None):
    """When the user closes the GUI, this function will handle closing all socket connections"""
    clientSock.close()
    GUI.quit()


"""Creating the GUI for out chatbot using Python's Tkinter library"""
GUI = tkinter.Tk()
GUI.title("TCP Chatbot")

frame = tkinter.Frame(GUI)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type here")
scrollbar = tkinter.Scrollbar(frame)  # scrollbar
# Following will contain the messages.
msg_list = tkinter.Listbox(frame, height=30, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
frame.pack()

entry_field = tkinter.Entry(GUI, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(GUI, text="Send", command=send)
send_button.pack()

GUI.protocol("WM_DELETE_WINDOW", exited)

#Checking parameteres
if (len(sys.argv) < 3):
  print("Usage: python3 "  + sys.argv[0] + " server_host" + "server_port")
  sys.exit(1)
assert(len(sys.argv) == 3)
server_port=int(sys.argv[2])
server_host=sys.argv[1]

address = (server_host, server_port)

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((server_host,server_port))

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # opens up the GUI
