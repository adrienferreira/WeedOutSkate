INP_VIDEO = "C:\\Users\\ferreira\\Documents\\LoudPeakDetect\\final.mp4"
FFMPEG_SRC = "./ffmpeg.exe"

TOP_X_LOUDEST = 40

STR_KEY_PTS_T = "pts_time"
STR_KEY_LAVFI = "lavfi.astats.Overall.RMS_level"

frame_dict = {"timestamp":0,"loud_db":0}
loud_frames = []

inp = open("log.txt", "r")
cur_frame = {}

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

out = open("output.csv", "w")

for l in loudest:
	out.write(FFMPEG_SRC + " ")
	out.write(" -ss " + str(l["timestamp"]))
	out.write(" -i " + INP_VIDEO)
	out.write(" -vframes 1 -q:v 2 ")
	out.write(" output_"+l["timestamp"].replace(".",'_')+".jpg ")
	out.write(" # " + str(l["loud_db"]))
	out.write("\n")

inp.close()
out.close();
