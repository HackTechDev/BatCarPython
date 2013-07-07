# 
# Interface de controle iRacer
#

import sys
import select
import tty
import termios
import bluetooth
import time
from evdev import InputDevice, categorize, ecodes
from Tkinter import *

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

def eventInfo(eventName, char, keysym, ctrl, shift):
    msg = "[" + char + "] " 
    if char == "z":
        msg += "Avancer Droit"
	sock.send('z')
	time.sleep(0.5);
    elif char == "s":
        msg += "Reculer Droit"
	sock.send('s')
	time.sleep(0.5);
    elif char == "q":
        msg += "Tourner Gauche"
	sock.send('q')
        time.sleep(0.5);
    elif char == "d":
        msg += "Tourner Droite"
	sock.send('d')
        time.sleep(0.5);
    elif char == "b":
        msg += "Bluetooth"
	sock.send('b')
        time.sleep(0.5);

    else:
	msg += "Inconnu"	

    return msg

def ignoreKey(event):
    ignoreSyms = [ "Shift_L", "Shift_R", "Control_L", "Control_R", "Caps_Lock" ]
    return (event.keysym in ignoreSyms)
    
def keyPressed(event):
    canvas = event.widget.canvas
    ctrl  = ((event.state & 0x0004) != 0)
    shift = ((event.state & 0x0001) != 0)
    if (ignoreKey(event) == False):
        canvas.data["info"] = eventInfo("keyPressed", event.char, event.keysym, ctrl, shift)
    if ((len(event.keysym) == 1) and (event.keysym.isalpha())):
        if (event.keysym not in canvas.data["pressedLetters"]):
            canvas.data["pressedLetters"].append(event.keysym)
    redrawAll(canvas)    


def redrawAll(canvas):
    canvas.delete(ALL)
    font = ("Arial", 16, "bold")
    info = canvas.data["info"]
    canvas.create_text(400, 50, text=info, font=font)

def init(canvas):
    canvas.data["info"] = "Mouvement"
    canvas.data["pressedLetters"] = [ ]
    redrawAll(canvas)

def run():

    bd_addr = "00:18:A1:12:16:C5"
    port = 1
    sock.connect((bd_addr, port))
    
    root = Tk()
    root.title("Controleur BatCar")
    canvas = Canvas(root, width=800, height=200)
    canvas.pack()
    root.canvas = canvas.canvas = canvas
    canvas.data = { }
    init(canvas)
    root.bind("<KeyPress>", keyPressed)
    root.mainloop()

run()
