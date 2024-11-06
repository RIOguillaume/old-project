from vision import picture_and_analyse
from ser import send_msg, get_msg, data_available
import time
from math import *
import cv2
import logging
import threading
import time

distance = 0
in_move = False
cap = cv2.VideoCapture(0)

def thread_image_analyse(name): 
    print("analyse d'image")
    while True:
        if not in_move:
            rot, value, coord_pts = picture_and_analyse(cap)
            if rot == -1 and value == -1:
                msg = "1l/0!"
            elif rot > 0 and abs(value) > 25 and (distance > 30 or distance == 0):
                msg = "1d/" + str(abs(value)) + "!"
            elif rot < 0 and abs(value) > 25 and (distance > 30 or distance == 0):
                msg = "1g/" + str(abs(value)) + "!"
            elif distance < 15 and distance > 2:
                msg = "1b/0!"
            else:
                msg = "1a/0!"
            send_msg(msg)
            msg = str(coord_pts)
            send_msg(msg)
    


def thread_uart(name):
    print("thread uart")
    while True: 
        if data_available():
            msg = get_msg()
            analyse_msg(msg)


def analyse_msg(msg):
    global distance
    global in_move
    msg_recon = ""
    msg_distance = False
    msg_inmove = False
    for i in msg:
        if msg_recon == "distance=":
            msg_recon = ""
            msg_distance = True
        elif msg_recon == "inmove=":
            msg_recon = ""
            msg_inmove = True
        msg_recon += chr(i)

    if msg_distance:
        distance = int(msg_recon)
    if msg_inmove:
        in_move = int(msg_recon)

if __name__ == "__main__":
    print("start all thread")
    x = threading.Thread(target=thread_image_analyse, args=("image",))
    y = threading.Thread(target=thread_uart, args=("uart",))
    x.start()
    y.start()
    
