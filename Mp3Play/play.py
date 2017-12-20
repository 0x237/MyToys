import os
import sys
import random


dirname = "C:\\Users\\870987\\Music"  # MP3文件所在文件夹，路径中不能包含空格
mincnt = 4  # 最小循环次数
maxcnt = 6  # 最大循环次数

# 读取命令行参数， 只传入MP3所在文件夹
if len(sys.argv) == 2:
	dirname = sys.argv[1]

# 读取命令行参数，传入MP3所在文件夹，最小循环次数，最大循环次数
if len(sys.argv) == 4:
	dirname = sys.argv[1]
	mincnt = sys.argv[2]
	maxcnt = sys.argv[3]

# 保证路径以\结尾
if dirname[-1] != "\\":
	dirname = dirname + "\\"
flist = os.listdir(dirname)
fcnt = len(flist)

oldindex = -1  # 上一首的序号

while 1:
	# 获取一个随机序号
	index = int(random.random()*10000)%fcnt

	# 避免两次随机播放相同的歌曲
	if index == oldindex:
		continue

	# 记录上一首的序号
	oldindex == index

	# 判断是否是MP3文件
	extname = os.path.splitext(flist[index])[1]
	if extname == ".mp3" or extname == ".MP3":
		print(flist[index])
		filepath = dirname + flist[index]

		# 复制播放文件到temp.mp3,主要是为了防止因为文件名原因引起ffplay使用问题
		open(dirname + "temp.mp3", "wb").write(open(filepath, "rb").read())	

		loopcnt = mincnt + int(random.random()*100)%(maxcnt - mincnt + 1)

		# 播放
		cmd = "ffplay -nodisp -hide_banner -autoexit -loop " + str(loopcnt) + " " + dirname + "temp.mp3"
		os.system(cmd)

