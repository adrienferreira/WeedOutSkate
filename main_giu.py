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

TOP_X_LOUDEST = 10
VID_EXT = ".mp4"

STR_KEY_PTS_T = "pts_time"
STR_KEY_LAVFI = "lavfi.astats.Overall.RMS_level"

FFMPEG_EXE = 'C:\\Users\\ferreira\\Documents\\LoudPeakDetect\\ffmpeg-20200115-0dc0837-win64-static\\bin\\ffmpeg', 

DELTA_BEF_AFT = 3.0

in_file = sys.argv[1]
cur_ts = 0
frame_img = None
log_file = "log__" + in_file.replace(".","") + ".txt"
kept_ts = []

def move_to_category(category, move_file):
	new_file = category + "/" + move_file
	if not os.path.exists(category):
		os.makedirs(category)

	if not os.path.exists(move_file):
		create_preview(cur_ts+VID_EXT)

	if os.path.exists(new_file):
		os.remove(new_file)
	os.rename(move_file, new_file)
	kept_ts.append(int(float(cur_ts)))

def create_preview(timestamp):
	cmd = [
		FFMPEG_EXE, 
		'-i', in_file, 
		'-ss', str(float(cur_ts) - DELTA_BEF_AFT), 
		'-to', str(float(cur_ts) + DELTA_BEF_AFT), 
		'-c', 'copy', 
		"-y",
		timestamp
	]
	subprocess.run(cmd, stderr=subprocess.STDOUT)

def cb_video():
	print("cb_bail")
	vid = cur_ts.replace(".","_") + VID_EXT
	create_preview(vid)
	os.startfile(vid)

def cb_fail():
	print("cb_bail")
	move_to_category(FOLD_FAIL,cur_ts.replace(".","_") + VID_EXT)
def cb_success():
	print("cb_success")
	move_to_category(FOLD_SUCC,cur_ts.replace(".","_") + VID_EXT)
def cb_other():
	print("cb_other")
	move_to_category(FOLD_OTHE,cur_ts.replace(".","_") + VID_EXT)
def cb_exit():
	print("cb_exit")
	os._exit(0)

my_cmd = [ 	FFMPEG_EXE, 
			"-i",  in_file,
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
	cur_ts = l["timestamp"]
	cmd_frame = [
		FFMPEG_EXE,
		"-ss", str(l["timestamp"]),
		"-i" , in_file,
		"-vframes", "1",
		"-vf","scale=800:-1",
		"-q:v", "2",
		"-y",
		frame_img,
	]
	subprocess.run(cmd_frame, stderr=subprocess.STDOUT)

	window = Tk()
	canvas = Canvas(window, width = 900, height = 500) 
	canvas.pack()

	T = Text(window, height=2, width=30)
	T.pack()
	T.insert(END, str(l["timestamp"]) + '\n' + ', '.join(map(str, kept_ts)))
	top = Frame(window)
	top.pack(side=TOP)

	b_video = Button(window, text="Video", command=cb_video)
	b_fail = Button(window, text="Bail",  command=cb_fail)
	b_success = Button(window, text="Success",  command=cb_success)
	b_other = Button(window, text="Other", command=cb_other)
	b_exit = Button(window, text="Exit", bg="salmon", command=cb_exit)

	b_video.pack(in_=top, side=LEFT)
	b_fail.pack(in_=top, side=LEFT)
	b_success.pack(in_=top, side=LEFT)
	b_other.pack(in_=top, side=LEFT)
	b_exit.pack(in_=top, side=LEFT)

	img = PhotoImage(file=frame_img)
	canvas.create_image(10, 10, anchor=NW, image=img)
	window.title("WeedOutSkateboard")
	window.mainloop()
