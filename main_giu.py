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

import sys
import subprocess
from tkinter import *
import cv2
import os

FOLD_TMP = "tmp"
FOLD_FAIL = "fail"
FOLD_SUCC = "success"
FOLD_OTHE = "other"

TOP_X_LOUDEST = 40

STR_KEY_PTS_T = "pts_time"
STR_KEY_LAVFI = "lavfi.astats.Overall.RMS_level"

FFMPEG_EXE = 'C:\\Users\\ferreira\\Documents\\LoudPeakDetect\\ffmpeg-20200115-0dc0837-win64-static\\bin\\ffmpeg', 

cur_file = sys.argv[1]
log_file = "log__" + cur_file

def cb_video():
	print("cb_bail")
	cmd = [
		FFMPEG_EXE, 
		'-i', cur_file, 
		'-ss', str(10), 
		'-to', str(15), 
		'-c', 'copy', 
		"-y",
		"python.mp4"
	]
	subprocess.run(cmd, stderr=subprocess.STDOUT)
	os.startfile("python.mp4")

def cb_bail():
	print("cb_bail")
def cb_success():
	print("cb_success")
def cb_other():
	print("cb_other")
def cb_discard():
	print("cb_discard")

my_cmd = [ 	FFMPEG_EXE, 
			"-i",  cur_file,
			"-af", "astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=" + log_file,
			"-f", "null", "-" ]

#subprocess.run(my_cmd, stderr=subprocess.STDOUT)
inp = open(log_file, "r")
cur_frame = {}
frame_dict = {"timestamp":0,"loud_db":0}
loud_frames = []

for x in inp:
	if "=-inf" in x:
		cur_frame = dict(frame_dict)
		continue

	if STR_KEY_PTS_T in x :
		cur_frame = dict(frame_dict)
		cur_frame["timestamp"] = x.split(STR_KEY_PTS_T + ":")[1].replace("\n",'')
	if STR_KEY_LAVFI in x :
		cur_frame["loud_db"] = float(x.split(STR_KEY_LAVFI + "=")[1].replace("\n",''))
		loud_frames.append(cur_frame)
loudest = sorted(loud_frames, reverse = True, key = lambda i: float(i["loud_db"]))


for l in loudest[:TOP_X_LOUDEST]:
	frame_img="output_"+l["timestamp"].replace(".",'_')+".gif"
	cmd_frame = [
		FFMPEG_EXE,
		"-ss", str(l["timestamp"]),
		"-i" , cur_file,
		"-vframes", "1",
		"-q:v", "2",
		frame_img,
	]
	subprocess.run(cmd_frame, stderr=subprocess.STDOUT)

	window = Tk()
	canvas = Canvas(window, width = 900, height = 500) 
	canvas.pack()

	T = Text(window, height=1, width=30)
	T.pack()
	T.insert(END, str(l["timestamp"]))
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

	img = PhotoImage(file=frame_img)
	canvas.create_image(10, 10, anchor=NW, image=img)  
	window.title("WeedOutSkateboard")
	window.mainloop()
