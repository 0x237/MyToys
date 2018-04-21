import sys
import os
import docx
import subprocess
import json
import re

# 转换视频播放秒数为ass文件要求的格式，获取片尾固定字幕的起始时间
def gettimestr(duration):
    secs = int(float(duration)) + 1
    secstr = ("0" + str(secs % 60))[-2:]
    minstr = ("0" + str(secs // 60))[-2:]

    secs1 = secs - 10
    secstr1 = ("0" + str(secs1 % 60))[-2:]
    minstr1 = ("0" + str(secs1 // 60))[-2:]
    return minstr1 + ":" + secstr1, minstr + ":" + secstr



dirname = input("输入目录：\n")

# 保证路径以\结尾
if dirname[-1] != "\\":
    dirname = dirname + "\\"

# 遍历文件夹内文件
flist = os.listdir(dirname)
for efile in flist:
    assname = os.path.splitext(efile)[0]
    extname = os.path.splitext(efile)[1]
    # 获取doc文档内容
    if extname == ".doc" or extname == ".docx":
        print("word文档：",efile)
        docpath = dirname+efile
        docfile = docx.Document(docpath)
        doctext = [paragraph.text for paragraph in docfile.paragraphs]

    # 获取视频文件相关信息
    if extname == ".mp4":
        print("视频文件：",efile)
        videopath = dirname+efile
        # 复制播放文件到temp.mp3,主要是为了防止因为文件名原因引起ffplay使用问题
        open("temp.mp4", "wb").write(open(videopath, "rb").read())    
        #运行ffprobe进程，将stdout解码为utf-8&转换为JSON 
        ffprobeOutput = subprocess.check_output("ffprobe -v quiet -print_format json -show_streams temp.mp4").decode("utf-8")
        ffprobeOutput = json.loads(ffprobeOutput)
        os.remove("temp.mp4")
        #查找高度和宽度
        videoheight = ffprobeOutput ['streams'] [0] ['height'] 
        videowidth = ffprobeOutput ['streams'] [0] ['width']
        duration = ffprobeOutput['streams'] [0] ['duration']
        print("视频分辨率：",videoheight,videowidth)
        print("视频时长：",duration)
        #print(ffprobeOutput)

# ass文件的头部信息
asshead = "[Script Info]\n" + \
    "; Script generated by Aegisub 3.2.2\n" + \
    "; http://www.aegisub.org/\n" + \
    "Title: Default Aegisub file\n" + \
    "ScriptType: v4.00+\n" + \
    "WrapStyle: 0\n" + \
    "ScaledBorderAndShadow: yes\n" + \
    "YCbCr Matrix: TV.601\n" + \
    "PlayResX: " + str(videowidth) + "\n" +\
    "PlayResY: " + str(videoheight)  + "\n"


asshead = asshead +    "[Aegisub Project Garbage]\n" + \
    "Audio File: " + videopath +"\n" + \
    "Video File: " + videopath +"\n" + \
    "Video AR Mode: 4\n" + \
    "Video AR Value: 1.777778\n" + \
    "Video Zoom Percent: 0.500000\n" + \
    "Scroll Position: 9\n" + \
    "Active Line: 15\n" + \
    "Video Position: 1208\n"

# ass文件的样式信息
assstyle = "[V4+ Styles]\n" + \
    "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n" + \
    "Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n" + \
    "Style: 柚子木-中文-1080P-2018,方正正粗黑_GBK,75,&H00D7E100,&HFFD7E100,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,5,0,2,0,0,15,1\n" + \
    "Style: 柚子木-注释-1080P-2018,方正正准黑_GBK,65,&H0000FFFF,&HFF00FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,8,0,0,15,1\n" + \
    "Style: 柚子木-中文-720P-2018,方正正粗黑_GBK,50,&H00D7E100,&HFFD7E100,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,3,0,2,0,0,10,1\n" + \
    "Style: 柚子木-注释-720P-2018,方正正准黑_GBK,43,&H0000FFFF,&HFF00FFFF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,2,0,8,0,0,10,1\n" 


isnormal = 0  # 判断视频文件的分辨率是否是可以处理的分辨率

# 对不同的分辨率的视频定义 \N的替代内容、片头尾、所用样式
if videowidth == 1920 and videoheight == 1080:
    isnormal = 1
    linesplit = "\\N{\\fnCalibri\\fs50\\c&HFFFFFF&\\3c&H000000&\\bord3\\shad0}"
    videohead = "Dialogue: 0,0:00:00.00,0:00:06.00,Default,,0,0,0,,{\\fad(0,500)}{\\an8\\pos(960,0)}{\\fscx1920\\fscy210\\c&H000000&\\1a&H80&\\bord0\\shad0}{\\p1}m 0 0 l 100 0 l 100 100 l 0 100 l 0 0\n" + \
        "Dialogue: 0,0:00:00.00,0:00:06.00,Default,,0,0,0,,{\\fad(0,500)}{\\an8\\pos(960,30)}{\\fn方正品尚黑简体\\b1\\fs70\\bord0\\shad0}{\\c&HFFFFFF&}手机应用市场搜索APP  [ {\\c&HD7E100&}柚tube{\\c&HFFFFFF&} ]\n" + \
        "Dialogue: 0,0:00:00.00,0:00:06.00,Default,,0,0,0,,{\\fad(0,500)}{\\an8\\pos(960,120)}{\\fn方正品尚黑简体\\b1\\fs70\\bord0\\shad0}{\\c&HFFFFFF&}听译: {\\c&HD7E100&}XXX    {\\c&HFFFFFF&}校正: {\\c&HD7E100&}XXX    {\\c&HFFFFFF&}时轴: {\\c&HD7E100&}XXX\n"
    footstart, footend = gettimestr(duration)
    videofoot = "Dialogue: 0,0:"+footstart+".00,0:"+footend+".00,Default,,0,0,0,,{\\fad(500,0)}{\\an8\\pos(960,0)}{\\fscx1920\\fscy210\\c&H000000&\\1a&H80&\\bord0\\shad0}{\\p1}m 0 0 l 100 0 l 100 100 l 0 100 l 0 0\n" + \
        "Dialogue: 0,0:"+footstart+".00,0:"+footend+".00,Default,,0,0,0,,{\\fad(500,0)}{\\an8\\pos(960,30)}{\\fn方正品尚黑简体\\b1\\fs70\\bord0\\shad0}{\\c&HFFFFFF&}微博 & 微信公众号 搜索 {\\c&HD7E100&}@柚子木字幕组\n" + \
        "Dialogue: 0,0:"+footstart+".00,0:"+footend+".00,Default,,0,0,0,,{\\fad(500,0)}{\\an8\\pos(960,120)}{\\fn方正品尚黑简体\\b1\\fs70\\bord0\\shad0}{\\c&HFFFFFF&}访问 {\\c&HD7E100&}www.uzimu.com {\\c&HFFFFFF&}下载 \n"
    styleusing = "柚子木-中文-1080P-2018"        

if videowidth == 1280 and videoheight == 720:
    isnormal = 1
    linesplit = "\\N{\\fnCalibri\\fs33\\c&HFFFFFF&\\3c&H000000&\\bord2\\shad0}"
    videohead = "Dialogue: 0,0:00:00.00,0:00:06.00,Default,,0,0,0,,{\\fad(0,500)}{\\an8\\pos(640,0)}{\\fscx1280\\fscy140\\c&H000000&\\1a&H80&\\bord0\\shad0}{\\p1}m 0 0 l 100 0 l 100 100 l 0 100 l 0 0\n" + \
        "Dialogue: 0,0:00:00.00,0:00:06.00,Default,,0,0,0,,{\\fad(0,500)}{\\an8\\pos(640,20)}{\\fn方正品尚黑简体\\b1\\fs45\\bord0\\shad0}{\\c&HFFFFFF&}手机应用市场搜索APP  [ {\\c&HD7E100&}柚tube{\\c&HFFFFFF&} ]\n" + \
        "Dialogue: 0,0:00:00.00,0:00:06.00,Default,,0,0,0,,{\\fad(0,500)}{\\an8\\pos(640,80)}{\\fn方正品尚黑简体\\b1\\fs45\\bord0\\shad0}{\\c&HFFFFFF&}听译: {\\c&HD7E100&}XXX    {\\c&HFFFFFF&}校正: {\\c&HD7E100&}XXX    {\\c&HFFFFFF&}时轴: {\\c&HD7E100&}XXX\n"
    footstart, footend = gettimestr(duration)
    videofoot = "Dialogue: 0,0:00:"+footstart+".00,0:"+footend+".00,Default,,0,0,0,,{\\fad(500,0)}{\\an8\\pos(640,0)}{\\fscx1280\\fscy140\\c&H000000&\\1a&H80&\\bord0\\shad0}{\\p1}m 0 0 l 100 0 l 100 100 l 0 100 l 0 0\n" + \
        "Dialogue: 0,0:00:"+footstart+".00,0:"+footend+".00,Default,,0,0,0,,{\\fad(500,0)}{\\an8\\pos(640,20)}{\\fn方正品尚黑简体\\b1\\fs45\\bord0\\shad0}{\\c&HFFFFFF&}微博 & 微信公众号 搜索 {\\c&HD7E100&}@柚子木字幕组\n" + \
        "Dialogue: 0,0:00:"+footstart+".00,0:"+footend+".00,Default,,0,0,0,,{\\fad(500,0)}{\\an8\\pos(640,80)}{\\fn方正品尚黑简体\\b1\\fs45\\bord0\\shad0}{\\c&HFFFFFF&}访问 {\\c&HD7E100&}www.uzimu.com {\\c&HFFFFFF&}下载 \n"
    styleusing = "柚子木-中文-720P-2018"

if not isnormal:
    print("视频分辨率特殊")
    end = input("回车键退出")
    sys.exit()

# ass文件的事件部分
assevent = "[Events]\n" + \
    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

assevent = assevent + videohead

# 将从doc文件中获取的内容合并起来，不再按段落分开
asstext = ""
for eachtext in doctext:
    asstext = asstext + eachtext + "\n"

# 确认格式符合要求
asstext, num = re.subn("([^\\x00-\\xff]) +(-)","\\1    \\2",asstext)
print("四空格替换数：",num)
asstext, num = re.subn("([^\\x00-\\xff]) +([^\\x00-\\xff])","\\1  \\2",asstext)
print("两空格替换数：",num)
asstext, num = re.subn("[“”]","\"",asstext)
print("中文引号替换数:",num)

# 将内容分行， 替换\N
asslines = asstext.split("\n\n")
for eachline in asslines:
    assevent = assevent + "Dialogue: 0,0:00:00.00,0:00:00.00,"+styleusing+",,0,0,0,," + (eachline.replace("\n",linesplit)) + "\n"

assevent = assevent + videofoot

# 保存
open(dirname + assname + ".ass", "w", encoding = "gb18030").write(asshead + assstyle + assevent)
# print(asshead + assstyle + assevent)

end = input("回车键退出")
sys.exit()

