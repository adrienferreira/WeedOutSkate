#import argparse
#import ffmpeg
#import sys
#
#(
#    ffmpeg
#    .input("./final.mp4", ss=10.0)
#    .output('pipe:', vframes=1, format='image2', vcodec='mjpeg')
#    .run(capture_stdout=True)
#)

from tkinter import *
import cv2
import os

def cb_video():
	os.startfile("out.mp4")
def cb_bail():
	print("cb_bail")
def cb_success():
	print("cb_success")
def cb_other():
	print("cb_other")
def cb_discard():
	print("cb_discard")

file = "output_41_4247.gif"

window = Tk()
canvas = Canvas(window, width = 900, height = 500) 
canvas.pack()

T = Text(window, height=1, width=30)
T.pack()
T.insert(END, "TimeStamp: 41.4247\n")
top = Frame(window)
top.pack(side=TOP)

b_video = Button(window, text="Video", command=cb_video)
b_bail = Button(window, text="Bail",  command=cb_bail)
b_success = Button(window, text="Success",  command=cb_success)
b_other = Button(window, text="Other", command=cb_other)
b_discard = Button(window, text="Discrad", bg="salmon", command=cb_discard)

b_video.pack(in_=top, side=LEFT)
b_bail.pack(in_=top, side=LEFT)
b_success.pack(in_=top, side=LEFT)
b_other.pack(in_=top, side=LEFT)
b_discard.pack(in_=top, side=LEFT)

img = PhotoImage(file=file)
canvas.create_image(10,10, anchor=NW, image=img)  
window.title("WeedOutSkateboard")
window.mainloop()
